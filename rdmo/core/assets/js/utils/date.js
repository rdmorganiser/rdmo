export const getDateFromDatetime = (datetime) => {
    const year = datetime.getFullYear()
    const month = String(datetime.getMonth() + 1).padStart(2, '0')
    const day = String(datetime.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}
