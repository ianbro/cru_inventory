$(document).ready(function(){
  populate_root_categories();
  $(".list__header.sub_category").each(function(){
    $(this).css("padding-left", "" + (parseInt($(this).attr("level")) * 10) + "px");
  });
  
  $(".item__name").live("click", function(){
    console.log($("div#item--" + $(this).attr("item-id")));
    $("div#item--" + $(this).attr("item-id")).slideToggle("fast");
  });
  $(".list__header").live("click", function(){
    $("div#category--" + $(this).attr("category-id")).slideToggle("fast");
  });
  $(".out_element__toggle").live("click", function(){
    $("#item--" + $(this).attr("item-id")).slideToggle("fast");
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
    });
  });
  
  $(".list__element > div, .list__content").hide();
});

function populate_root_categories() {
  for (var i = 0; i < window.root_categories.length; i++) {
    var cat = window.root_categories[i];
    if ("categories" in cat) {
      var len = cat.categories.length;
      // for some reason, at some point, cat.categories here is undefined.
      for (var j = 0; j < len; j++) {
        var sub_cat = cat.categories[j];
        var sub_cats_html = populate_category(sub_cat);
        $("#category--" + cat.pk).append(sub_cats_html);
      }
    } else {
      for (var j = 0; j < cat.items.length; j++) {
        var item = cat.items[j];
        var items_html = populate_item(item);
        $("#category--" + cat.pk).append(items_html);
      }
    }
  }
}

function populate_category(category) {
  var cat_container = "\
    <div class=\"list__header sub_category\" level=\"" + category.level + "\" id=\"header--" + category.pk + "\" category-id=\"" + category.pk + "\"> \n\t\
      <h3>" + category.name + "</h3> \n\
    </div> \n\
    <div class=\"list__content\" id=\"category--" + category.pk + "\"> \n"
  //   console.log($("#category--" + parent_id));
  // $("#category--" + parent_id).append(cat_container);
  if ("categories" in category) {
    for (var i = 0; i < category.categories.length; i++) {
      var cat = category.categories[i];
      cat_container = cat_container + populate_category(cat);
    }
  } else {
    for (var i = 0; i < category.items.length; i++) {
      item = category.items[i];
      cat_container = cat_container + populate_item(item);
    }
  }
  cat_container = cat_container + "\n</div> <!-- " + category.name + " and " + category.pk + " -->\n"
  return cat_container
}

function populate_item(item){
  var item_container = "\
    <div class=\"list__element\" id=\"item_in-" + item.pk + "\"> \n\
      <h4 class=\"item__name\" item-id=\"" + item.pk + "\">" + item.name + "</h4> \n\
      <div id=\"item--" + item.pk + "\"> \n\
        <form method=\"post\" action=\"/inventory/checkout/\"> \n\
          " + window.csrf + " \n\
          <p class=\"item__desc\">" + item.description + "</p> \n\
          <p class=\"item__amount\">" + item.amount_left + " of " + item.total_amount + " left. Take out: \n\
            <input type=\"number\" name=\"amount\" id=\"" + item.id + "--amount\" value=\"1\" min=\"1\" max=\"" + item.amount_left + "\"></input> \n\
          </p> \n\
          <button name=\"item_id\" type=\"submit\" class=\"submit_checkout\" value=\"" + item.pk + "\">Checkout</button> \n\
        </form> \n\
      </div> \n\
    </div>\n"
  return item_container;
}