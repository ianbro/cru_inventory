$(document).ready(function(){
  $(".list__element > div").hide();
  
  $(".item__name").live("click", function(){
    $(this).siblings("div").toggle();
  });
  
  $(".submit_checkin").live("click", function() {
    $.getJSON("/inventory/checkin/" + $(this).val() + "/", function(data){
      if (data.success == true) {
        window.location.reload();
      } else {
        console.log(data);
      }
    });
  })
  
  $(".useup_item").live("click", function() {
    $.getJSON("/inventory/useup/" + $(this).val() + "/", function(data){
      if (data.success == true) {
        window.location.reload();
      } else {
        console.log(data);
      }
    })
  });
});