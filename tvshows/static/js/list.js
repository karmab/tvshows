function tvshowslist() {
    $.ajax({
         type: "GET",
          url: '/tvshows',
          success: function(data) {
            $('#tvshows').html(data);
          }
    });
    $('[data-toggle="tooltip"]').tooltip();
}
