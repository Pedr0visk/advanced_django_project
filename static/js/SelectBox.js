(function ($) {
  'use strict';

  const SelectBox = {
    cache: {},

    init: function (id) {
      let box = document.getElementById(id);
      let node;
      SelectBox.cache[id] = [];
      let cache = SelectBox.cache[id];
      let boxOptions = box.options;
      let boxOptionsLength = boxOptions.length;
      for (let i = 0, j = boxOptionsLength; i < j; i++) {
        node = boxOptions[i];
        cache.push({ value: node.value, text: node.text, displayed: 1 })
      }
    },

    redisplay: function (id) {
      // Repopulate HTML select box from cache
      let box = document.getElementById(id);
      let node;
      $(box).empty(); // clear all options
      let new_options = box.outerHTML.slice(0, -9); // grab just the opening tag
      let cache = SelectBox.cache[id];
      for (let i = 0, j = cache.length; i < j; i++) {
        node = cache[i];
        if (node.displayed) {
          let new_option = new Option(node.text, node.value, false, false);
          // Shows a tooltip when hovering over the option
          new_option.setAttribute("title", node.text);
          new_options += new_option.outerHTML;
        }
      }
      new_options += '</select>';
      box.outerHTML = new_options;
    },

    cache_contains: function (id, value) {
      // Check if an item is contained in the cache
      let node;
      let cache = SelectBox.cache[id];
      for (let i = 0, j = cache.length; i < j; i++) {
        node = cache[i];
        if (node.value === value) {
          return true;
        }
      }
      return false;
    },

    delete_from_cache: function (id, value) {
      let node, delete_index = null;
      let cache = SelectBox.cache[id];
      for (let i = 0, j = cache.length; i < j; i++) {
        node = cache[i];
        if (node.value === value) {
          delete_index = i;
          break;
        }
      }
      cache.splice(delete_index, 1);
    },

    add_to_cache: function (id, option) {
      SelectBox.cache[id].push({ value: option.value, text: option.text, displayed: 1 });
    },

    move: function (from, to) {
      let from_box = document.getElementById(from);
      let option;
      let boxOptions = from_box.options;
      let boxOptionsLength = boxOptions.length;

      for (let i = 0, j = boxOptionsLength; i < j; i++) {
        option = boxOptions[i];
        let option_value = option.value;
        if (option.selected && SelectBox.cache_contains(from, option_value)) {
          SelectBox.add_to_cache(to, { value: option_value, text: option.text, displayed: 1 });
          SelectBox.delete_from_cache(from, option_value);
        }
      }
      SelectBox.redisplay(from);
      SelectBox.redisplay(to);
    },
    select_all: function (id) {
      let box = document.getElementById(id);
      let boxOptions = box.options;
      let boxOptionsLength = boxOptions.length;
      for (let i = 0; i < boxOptionsLength; i++) {
        boxOptions[i].selected = 'selected';
      }
    }
  };

  window.SelectBox = SelectBox
})(jQuery)
