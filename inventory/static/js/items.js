$(document).ready(function(){
  $(".list__element > div").hide();
  
  $(".item__name").live("click", function(){
    $(this).siblings("div").toggle();
  });
  
  $(".submit_checkin").live("click", function() {
    $.getJSON("/inventory/checkin/" + $(this).val() + "/", function(data){
      if (data.success == true) {
        window.location.reload();
      }
    });
  })
  
  $(".submit_checkout").live("click", function() {
    
  });
});