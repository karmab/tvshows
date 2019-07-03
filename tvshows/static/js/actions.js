function tvshowcreate(){
  $("#wheel").show();
  name = $("#name").val();
  finale = $("#finale").val();
  data = {'name': name, 'finale': finale};
  $.ajax({
       type: "POST",
        url: '/new',
        data: data,
        success: function(data) {
            $("#wheel").hide();
            if (data.result == 'success') {
                $('.top-right').notify({message: { text: "Tvshow "+name+" created!!!" }, type: 'success'}).show();
                tvshowslist();
            } else {
                $('.top-right').notify({message: { text: "Tvshow "+name+" not created because "+data.reason }, type: 'danger'}).show();
            };
        }
    });
}

function tvshowdelete(name){
  $("#wheel").show();
  data = {'name': name};
  //var r = confirm("Are you sure you want to delete this VM?");
  //if (r != true) {
  //  return ;
  //}
  $.ajax({
       type: "POST",
        url: '/delete',
        data: data,
        success: function(data) {
            $("#wheel").hide();
            if (data.result == 'success') {
                $('.top-right').notify({message: { text: "Show "+name+" deleted!!!" }, type: 'success'}).show();
                tvshowslist();
            } else {
                $('.top-right').notify({message: { text: "Show "+name+" not deleted because "+data.reason }, type: 'danger'}).show();
            };
        }
    });
}
