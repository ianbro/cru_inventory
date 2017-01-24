class ListItemsOut {
  constructor(category_id) {
    this.listId = "#list_items_in"
    this.shown = false;
    
    this.show = function() {
      $(".js-extras").slideUp("fast");
      $("#items_out_container").slideDown("fast");
      this.shown = true;
    }
    
    this.close = function() {
      $("#items_out_container").slideUp("fast");
      this.shown = false;
    }
    
    this.initialize = function() {
      var component = this;
      
      var url = "/inventory/ajax_get_list_items_out_json";
      var data = [];
      $.getJSON(url, function(json) {
        for (var i = 0; i < json.data.length; i++) {
          data.push(json.data[i]);
        }
        component.initialize_fuzzy_search(data);
        component.fuzzy_search.initialize();
        component.initialize_jquery();
      });
    }
    
    this.initialize_jquery = function() {
      var component = this;

      $(document).ready(function() {
        $(document).on("click", ".js-itemout_display", function() {
          $(this).siblings(".js-itemout_info").slideToggle("fast");
        });
      });
      
      $("#show_items_out").click(function() {
        if (component.shown) {
          component.close();
        } else {
          component.show();
        }
      });
    }
    
    this.initialize_fuzzy_search = function(data) {
      var build_row = function(html) {
        $(this.listId).append(html);
      };
      var keys = ['item.name'];
      var search_id = "search-items-out";
      var list_id = "list-items-out";
      var mass_build = "/inventory/ajax_get_list_items_out_html";
      
      this.fuzzy_search = new FuzzySearch(data, keys, search_id, list_id, build_row, null, mass_build);
    }
  }
}