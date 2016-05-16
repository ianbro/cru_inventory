$(document).ready(function(){
  populate_root_categories();
  
  $(".list__element > div").hide();
  
  console.log(window.root_categories);
  console.log(window.csrf);
  
  $(".item__name").live("click", function(){
    $(this).siblings("div").toggle();
  });
  $(".list__header").live("click", function(){
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

function populate_root_categories() {
  for (var i = 0; i < window.root_categories.length; i++) {
    var cat = window.root_categories[i];
    if ("categories" in cat) {
      var len = cat.categories.length;
      // for some reason, at some point, cat.categories here is undefined.
      for (var j = 0; j < len; j++) {
        var sub_cat = cat.categories[j];
        $("#category--" + cat.pk).append(populate_category(sub_cat));
      }
    } else {
      for (var j = 0; j < cat.items.length; j++) {
        var item = cat.items[j];
        $("#category--" + cat.pk).append(populate_item(item));
      }
    }
  }
}

function populate_category(category) {
  var cat_container = "\
    <div class=\"list__header\"> \
      <h3>" + category.name + "</h3> \
    </div> \
    <div class=\"list__content\" id=\"category--" + category.pk + "\"> \n"
  //   console.log($("#category--" + parent_id));
  // $("#category--" + parent_id).append(cat_container);
  if ("categories" in category) {
    for (var i = 0; i < category.categories.length; i++) {
      var cat = category.categories[i];
      cat_container = cat_container + populate_category(cat) + "</div>";
    }
  } else {
    for (var i = 0; i < category.items.length; i++) {
      item = category.items[i];
      cat_container = cat_container + populate_item(item) + "</div>";
    }
  }
  return cat_container
}

function populate_item(item){
  var item_container = "\
    <div class=\"list__element\" id=\"item_in-" + item.pk + "\"> \
      <h4 class=\"item__name\">" + item.name + "</h4> \
      <div> \
        <form method=\"post\" action=\"/inventory/checkout/\"> \
          " + window.csrf + " \
          <p class=\"item__desc\">" + item.description + "</p> \
          <p class=\"item__amount\">" + item.amount_left + " of " + item.total_amount + " left. Take out: \
            <input type=\"number\" name=\"amount\" id=\"" + item.id + "--amount\" value=\"1\" min=\"1\" max=\"" + item.amount_left + "\"></input> \
          </p> \
          <button name=\"item_id\" type=\"submit\" class=\"submit_checkout\" value=\"" + item.pk + "\">Checkout</button> \
        </form> \
      </div> \
    </div>"
  return item_container;
}