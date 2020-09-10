(function ($) {
  'use strict';

  function findForm(node) {
    // returns the node of the form containing the given node
    if (node.tagName.toLowerCase() !== 'form') {
      return findForm(node.parentNode);
    }
    return node;
  }

  window.SelectFilter = {
    init: function (field_id, field_name, is_stacked) {
      let from_box = document.getElementById(field_id),
        to_box = document.getElementById('to_box');

      from_box.id += '_from';
      to_box.id = field_id + '_to';

      from_box.setAttribute('name', from_box.getAttribute('name') + '_old');

      // buttons
      let add_link = document.getElementById('selectorAdd');
      let remove_link = document.getElementById('selectorRemove');

      // Event handlers for the select box filter interface
      var move_selection = function (e, elem, move_func, from, to) {
        e.preventDefault();

        if (elem.className.indexOf('active') !== -1) {
          move_func(from, to);
        }
      };

      add_link.addEventListener('click', function (e) {
        move_selection(e, this, SelectBox.move, field_id + '_from', field_id + '_to');
      });

      remove_link.addEventListener('click', function (e) {
        move_selection(e, this, SelectBox.move, field_id + '_to', field_id + '_from');
      });

      findForm(from_box).addEventListener('submit', function () {
        SelectBox.select_all(field_id + '_to');
      });

      // Init cache for select boxes
      SelectBox.init(field_id + '_from');
      SelectBox.init(field_id + '_to');

      // Move selected from_box options to to_box
      SelectBox.move(field_id + '_from', field_id + '_to');

    }
  }

  window.addEventListener('load', function (e) {
    $('select.selectfilter').each(function () {
      let $el = $(this), data = $el.data();

      SelectFilter.init($el.attr('id'), data.fieldName, parseInt(data.isStacket, 10));
    });
  });
})(jQuery);
