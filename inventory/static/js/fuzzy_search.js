class FuzzySearch {
    
    /*
     * Credit goes to Nathan Papes for designing this.
     * 
     * This fuzzy search allows you to dynamically add a search
     * function to a list of data.
     * 
     * Parameters:
     * data - list of data to be searchable. Each item must be
     *        javascript object.
     * keys - fields to be compared to on a search. These must be
     *        existing fields in each object contained in data.
     * search_id - html id of the search input field. **Note: do not
     *             include the '#' in the id selector.
     * list_id - html id of the area on the page that will contain the
     *           data. **Note: do not include the '#' in the id selector.
     * build_row - function that builds an element and adds it to the
     *             area on the page that contains the data. build_row
     *             must accept a javascript object. That element will
     *             be an element in data.
     * sort_key - key in data for data to be sorted on
     *            mass_build - For larger lists, We'll want to get the html for the
     *            items all at once instead of for each item. if mass_build is null,
     *            assume that we're not using this way of getting the html. otherwise,
     *            assume mass_build is a url that returns the html needed.
     */
    constructor(data, keys, search_id, list_id, build_row, sort_key=null, mass_build=null){
        this.data = data;
        this.keys = keys;
        this.fuse = new Fuse(this.data, {
            caseSensitive: false,
            includeScore: false,
            shouldSort: true,
            threshold: 0.4,
            location: 0,
            distance: 100,
            maxPatternLength: 32,
            keys: this.keys,
        });
        this.listId = "#" + list_id;
        this.searchId = "#" + search_id
        this.buildRow = build_row
        this.massBuild = mass_build;
        this.buildList = function(array) {
            if (sort_key != null) {
              array.sort(this.compareElements)
            }
            
            if (this.massBuild != null) {
              this.massBuildList(array);
            } else {
              var br = this.buildRow
              $.each(array, function(index, object){
                  br(object);
              });
            }
        };
        this.massBuildList = function(array) {
            if (array.length <= 0) {
              return;
            }
            
            var fs = this;
            
            var ids = "" + array[0].type + ":" + array[0].pk;
            for (var i = 1; i < array.length; i++) {
              ids = ids + ";" + array[i].type + ":" + array[i].pk;
            }
            
            $.ajax({
              url: fs.massBuild,
              method: "GET",
              dataType: "html",
              data: {"ids": ids},
              success: function(html) {
                fs.buildRow(html);
              }
            });
        }
        this.evaluate = function (fuzzySearch){
            var result = fuzzySearch.fuse.search($(fuzzySearch.searchId).val());
            $(fuzzySearch.listId + " .fuzzy_search__element").remove();
            
            // if no filer input length == 0, show all items
            if($(fuzzySearch.searchId).val().length == 0) {
                fuzzySearch.buildList(fuzzySearch.data);
            }
            else {
                // red text color on no results
                if(result.length == 0) {
                    $(fuzzySearch.searchId).css("color", "red");
                    fuzzySearch.buildList(result);
                }
                // black text color with results
                else {
                    $(fuzzySearch.searchId).css("color", "black");
                    fuzzySearch.buildList(result);
                }
            }
        };
        this.initialize = function(){
            var fuzzySearch = this;
            var doSearch = this.evaluate;
            $(this.searchId).keyup(function() {
              doSearch(fuzzySearch);
            });
            $(this.searchId).keyup();
        };
        this.get_item = function(search_by, value) {
          if (search_by == "id") {
            return this.data[this.get_item_index(value)];
          } else if (search_by == "index") {
            return this.data[value];
          } else {
            return {};
          }
        }
        this.get_item_index = function(id) {
          for (var i = 0; i < this.data.length; i++) {
            var item = this.data[i]
            if (item.pk == id) {
              return i;
            }
          }
          return null;
        }
        this.refresh = function(){
          this.fuse = new Fuse(this.data, {
              caseSensitive: false,
              includeScore: false,
              shouldSort: true,
              threshold: 0.4,
              location: 0,
              distance: 100,
              maxPatternLength: 32,
              keys: this.keys,
          });
          $(this.searchId).keyup();
        }
        this.remove_item = function(item_json){
            var index = this.get_item_index(item_json.pk);
            this.data.splice(index, 1);
            this.refresh();
        }
        this.add_item = function(item_json){
            this.data.push(item_json);
            this.refresh();
        }
        this.compareElements = function(a, b) {
          var keyType = typeof a[sort_key];
          if (keyType == "number") {
            return a[sort_key] - b[sort_key];
          } else if (keyType == "string") {
            var asciiFirst = a[sort_key].charAt(0).toLowerCase().charCodeAt(0);
            var asciiSecond = b[sort_key].charAt(0).toLowerCase().charCodeAt(0);
            return asciiFirst - asciiSecond;
          }
        }
    }
}