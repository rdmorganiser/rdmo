;(function () {
  $("#toast").toast({ delay: 2000 })

  htmx.on("showMessage", (e) => {
    $("#toast-body").text(e.detail.value)
    $("#toast").toast("show")
  })
})()
