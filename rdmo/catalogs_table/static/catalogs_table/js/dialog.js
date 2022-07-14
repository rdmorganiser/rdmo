;(function () {
    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal for BS 3.41
      if (e.detail.target.id == "dialog") {
        // $('#' + 'catalogs' + '-form-modal').modal('show');
        $("#modal").modal("show")
      }
      else {
        // console.log("htmx:afterSwap", e)
        // console.log("htmx:afterSwap detail", e.detail.parameters)
      }
    })
  
    htmx.on("htmx:beforeSwap", (e) => {
      // console.log("htmx:beforeSwap", e)
      // Empty response targeting #dialog => hide the modal
      // console.log('Empty response targeting #dialog => hide the modal')
      // console.log('Target id == ', e.detail.target.id)
      // console.log('Detail STatus: ', e.detail.xhr.status)
      if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        $("#modal").modal("hide")
        e.detail.shouldSwap = false
        // console.log('shouldSwap = false, should be hidden?')
      }
      else {
        // console.log('ELSE ', e.detail.target.id) //'Detail: ', e.detail.xhr.response)
      }
    })
  
    // Remove dialog content after hiding
    $("#modal").on("hidden.bs.modal", () => {
      $("#dialog").empty()
    })
  })()
  