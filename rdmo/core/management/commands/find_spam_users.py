import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rdmo.projects.models import Membership


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-t", "--timespan",
            default=2, type=int,
            help=(
                "timespan in seconds between two joining users, "
                "less than the given value is considered to be suspicious, "
                "default is 2"
            )
        )
        parser.add_argument(
            "-n", "--occurrence",
            default=3, type=int,
            help=(
                "number of sequentially occurring timespan "
                "violations at which users are put into the "
                "potential spam users list, default is 3"
            )
        )
        parser.add_argument(
            "-p", "--print",
            action="store_true",
            help="print found users, don't save them to csv"
        )
        parser.add_argument(
            "-o", "--output_file",
            default="potential_spam_users.csv",
            help="output file, default is 'potential_spam_users.csv'"
        )

    def save_csv(self, data, filename):
        if data:
            with open(filename, "w", newline="", encoding="utf-8") as data_file:
                csv_writer = csv.writer(data_file)
                csv_writer.writerow(list(data[0].keys()))
                for user in data:
                    csv_writer.writerow(user.values())
            print(f"List written to {filename}")

    def print_file(self, filename):
        with open(filename) as f:
            content = f.read()
            print(content)

    def get_users_having_projects(self):
        memberships = Membership.objects.all().values_list("user", flat=True)
        return list(memberships)

    def append_to_group(self, group_list, group_count, user, list_users_having_projects):
        date_string = "%Y-%m-%dT%H:%M:%S.%f"
        last_login = user["last_login"].strftime(date_string) if user["last_login"] else None

        has_project = user["id"] in list_users_having_projects
        group_list[group_count].append(
            {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "date_joined": user["date_joined"].strftime(date_string),
                "last_login": last_login,
                "has_project": has_project,
            }
        )
        return group_list

    def find_potential_spam_users(self, timespan, occurrence):
        list_users_having_projects = self.get_users_having_projects()
        arr = [
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": user.date_joined,
                "unix_joined": user.date_joined.timestamp(),
                "email": user.email,
                "last_login": user.last_login,
            }
            for user in User.objects.all().order_by("date_joined")
        ]

        grouped = {}
        group_count = 0
        for idx, user in enumerate(arr):
            prev = arr[idx - 1] if idx > 0 else None
            diff = user["unix_joined"] - prev["unix_joined"] if prev else timespan

            if prev and diff >= timespan:
                group_count += 1

            grouped.setdefault(group_count, [])
            grouped = self.append_to_group(grouped, group_count, user, list_users_having_projects)

        grouped_clean = {k: v for k, v in grouped.items() if len(v) > occurrence}
        potential_spam_users = [user for group in grouped_clean.values() for user in group]

        return potential_spam_users, len(list_users_having_projects)

    def handle(self, *args, **options):
        no_total_users = User.objects.count()
        print(f"Total no of users: {no_total_users}")

        potential_spam_users, no_users_having_projects = self.find_potential_spam_users(
            options["timespan"], options["occurrence"]
        )

        percentage = (100 / no_total_users) * len(potential_spam_users) if no_total_users else 0
        print(
            f"Potential spam users: {len(potential_spam_users)}  {percentage:.2f}% / "
            f"of which have at least one project {no_users_having_projects}"
        )

        self.save_csv(potential_spam_users, options["output_file"])
        if options["print"]:
            self.print_file(options["output_file"])
