$(document).ready(function(){
  $(".list__header.sub_category").each(function(){
    $(this).css("padding-left", "" + (parseInt($(this).attr("level")) * 10) + "px");
  });
  $(".header_all_out").live("click", function(){
    $(".content_all_out").slideToggle("fast");
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
});

class ItemsInExtrasComponent {
  constructor() {
    this.item = null;
    this.show = function(item) {
      $(".js-itemin_name").html(item.name);
      $(".js-itemin_description").html(item.description);
      $(".js-itemin_total_amount").html(item.total_amount);
      $(".js-itemin_amount_left").html(item.amount_left);
      $(".js-itemin_category").html(item.category__name);
      $(".js-itemin_date_added").html(item.date_added);
      
      this.populate_fuzzy_search(item.records);
      
      $("#itemsin_extras_container").slideDown("fast");
      this.item = item;
    }
    
    this.hide = function() {
      $("#itemsin_extras_container").slideUp("fast");
      
      $(".js-itemin_name").html("NONE");
      $(".js-itemin_description").html("NONE");
      $(".js-itemin_total_amount").html("NONE");
      $(".js-itemin_amount_left").html("NONE");
      $(".js-itemin_category").html("NONE");
      $(".js-itemin_date_added").html("NONE");
      $("#search_records_per_item").val("");
      this.populate_fuzzy_search([]);
      $("#itemin_records_list").html();
      this.item = null;
    }
    
    this.populate_fuzzy_search = function(records) {
      this.record_search.data = records;
      this.record_search.refresh();
    }
    
    this.initialize_fuzzy_search = function() {
      var build_row = function(html) {
        $(this.listId).append(html);
      };
      var keys = ['person'];
      var search_id = "search_records_per_item";
      var list_id = "itemin_records_list";
      var mass_build = "/inventory/ajax_get_records_by_item_html";
      
      this.record_search = new FuzzySearch([], keys, search_id, list_id, build_row, null, mass_build);
      this.record_search.initialize();
    }
    this.initialize_fuzzy_search();
    
    this.initialize_jquery = function() {
      var component = this;
      $(document).on("click", "#close_itemin_extras", function() {
        component.hide();
      });
    }
    this.initialize_jquery();
  }
}