function tvshowcreate(){
  name = $("#name").val();
  finale = $("#finale").val();
  data = {'name': name, 'finale': finale};
  $.ajax({
       type: "POST",
        url: '/new',
        data: data,
        success: function(data) {
            if (data.result == 'success') {
                $('.top-right').notify({message: { text: "Tvshow "+name+" created!!!" }, type: 'success'}).show();
            } else {
                $('.top-right').notify({message: { text: "Tvshow "+name+" not created because "+data.reason }, type: 'danger'}).show();
            };
        }
    });
}
