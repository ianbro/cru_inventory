class ListItemsIn {
  constructor(category_id) {
    this.catClass = ".js-category";
    this.itemClass = ".js-submit_itemcheckout";
    
    this.render = function() {
      var component = this;
      
      var GET_data = [];
      var list_selector = "#root_list";
      if (category_id != null) {
        // Then this is the root (e.g. no parent category)
        list_selector = "#" + category_id;
        var GET_data = {
          cat_id: category_id
        };
      }
      
      if ($(list_selector).length > 0) {
        // This category is already open.
        return;
      }
      
      var url = "/inventory/ajax_get_list_html/";
      $.ajax({
        url: url,
        method: "GET",
        data: GET_data,
        dataType: "html",
        success: function(html) {
          $("#itemsin_navigation").append(html);
          component.component_id = list_selector;
          component.initialize();
        }
      });
    }
    
    this.refresh = function() {
      var component = this;
      
      var url = "/inventory/ajax_get_items_by_category";
      if (category_id != null) {
        url = url + "?cat_id=" + category_id;
      }
      var data = [];
      $.getJSON(url, function(json) {
        for (var i = 0; i < json.items.length; i++) {
          data.push(json.items[i]);
        }
        for (var i = 0; i < json.sub_categories.length; i++) {
          data.push(json.sub_categories[i]);
        }
        component.fuzzy_search.data = data
        component.fuzzy_search.refresh();
      });
    }
    
    this.close = function() {
      $(this.component_id).remove();
      if (this.openCategory) {
        this.openCategory.close();
        delete this.openCategory;
      }
    }
    
    this.initialize = function() {
      var component = this;
      
      var url = "/inventory/ajax_get_items_by_category";
      if (category_id != null) {
        url = url + "?cat_id=" + category_id;
      }
      var data = [];
      $.getJSON(url, function(json) {
        for (var i = 0; i < json.items.length; i++) {
          data.push(json.items[i]);
        }
        for (var i = 0; i < json.sub_categories.length; i++) {
          data.push(json.sub_categories[i]);
        }
        component.initialize_fuzzy_search(data);
        component.fuzzy_search.initialize();
        component.initialize_jquery();
      });
    }
    
    this.initialize_jquery = function() {
      var component = this;
      var category_selector = component.component_id + " " + component.catClass;
      var item_selector = component.component_id + " " + component.itemClass;
      var iextras_selector = component.component_id + " " + ".js-item_toggle_extras";
      
      $(document).on("click", category_selector, function() {
        var new_category_id = $(this).attr("category-id");
        var component = this;
        
        if (component.openCategory) {
          component.openCategory.close();
        }
        component.openCategory = new ListItemsIn(new_category_id);
        component.openCategory.render();
      });
      
      $(document).on("click", item_selector, function() {
        component.submit(component.get_input(this));
      });
      
      $(document).on("click", iextras_selector, function() {
        var itemid = $(this).attr("item-id");
        var item = component.fuzzy_search.get_item("id", itemid);
        window.itemsinExtrasComponent.show(item);
      });
    }
    
    this.initialize_fuzzy_search = function(data) {
      var build_row = function(html) {
        $(this.listId).append(html);
      };
      var keys = ['name'];
      var search_id = this.component_id.substring(1) + " .search-items-in";
      var list_id = this.component_id.substring(1) + " .list-items-in";
      var mass_build = "/inventory/ajax_get_items_by_category_html";
      
      this.fuzzy_search = new FuzzySearch(data, keys, search_id, list_id, build_row, null, mass_build);
    }
    
    this.get_input = function(submit_button) {
      var name = $(submit_button).parent().parent().find(".item__checkout_name").val();
      var amount = $(submit_button).parent().parent().find(".item__amount_input").val();
      var itemid = $(submit_button).val();
      
      return {
        item_id: itemid,
        person: name,
        amount: amount,
        csrfmiddlewaretoken: window.csrf
      };
    }
    
    this.submit = function(input) {
      var component = this;
      var url = "/inventory/checkout/";
      $.ajax({
        url: url,
        type: "POST",
        data: input,
        dataType: "json",
        success: function(json) {
          window.itemsOutList.fuzzy_search.add_item(json.item_record);
          component.refresh();
        }
      });
    }
  }
}

$(document).ready(function() {
  $(document).on("click", ".js_itemin", function() {
    $(this).parent().parent().find(".js-item_info").slideToggle("fast");
  });
});