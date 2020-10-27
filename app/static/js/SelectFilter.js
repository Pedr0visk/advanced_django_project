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
            from_box.removeAttribute('required');
            // buttons
            let add_link = document.getElementById(`${field_id}_add_link`);
            let remove_link = document.getElementById(`${field_id}_remove_link`);

            // filter input
            let filter_input = document.getElementById(`${field_id}_input`);

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

            filter_input.addEventListener('keypress', function (e) {
                SelectFilter.filter_key_press(e, field_id);
            });

            filter_input.addEventListener('keyup', function (e) {
                SelectFilter.filter_key_up(e, field_id);
            });

            filter_input.addEventListener('keydown', function (e) {
                SelectFilter.filter_key_down(e, field_id);
            });

            // on submit
            findForm(from_box).addEventListener('submit', function () {
                SelectBox.select_all(field_id + '_to');
            });

            // Init cache for select boxes
            SelectBox.init(field_id + '_from');
            SelectBox.init(field_id + '_to');

            // Move selected from_box options to to_box
            SelectBox.move(field_id + '_from', field_id + '_to');

        },
        filter_key_press: function (event, field_id) {
            let from = document.getElementById(field_id + '_from');
            // don't submit form if user pressed Enter
            if ((event.which && event.which === 13) || (event.keyCode && event.keyCode === 13)) {
                from.selectedIndex = 0;
                SelectBox.move(field_id + '_from', field_id + '_to');
                from.selectedIndex = 0;
                event.preventDefault();
                return false;
            }
        },
        filter_key_up: function (event, field_id) {
            const from = document.getElementById(field_id + '_from');
            const temp = from.selectedIndex;
            SelectBox.filter(field_id + '_from', document.getElementById(field_id + '_input').value);
            from.selectedIndex = temp;
            return true;
        },
        filter_key_down: function (event, field_id) {
            let from = document.getElementById(field_id + '_from');
            // right arrow -- move across
            if ((event.which && event.which === 39) || (event.keyCode && event.keyCode === 39)) {
                let old_index = from.selectedIndex;
                SelectBox.move(field_id + '_from', field_id + '_to');
                from.selectedIndex = (old_index === from.length) ? from.length - 1 : old_index;
                return false;
            }
            // down arrow -- wrap around
            if ((event.which && event.which === 40) || (event.keyCode && event.keyCode === 40)) {
                from.selectedIndex = (from.length === from.selectedIndex + 1) ? 0 : from.selectedIndex + 1;
            }
            // up arrow -- wrap around
            if ((event.which && event.which === 38) || (event.keyCode && event.keyCode === 38)) {
                from.selectedIndex = (from.selectedIndex === 0) ? from.length - 1 : from.selectedIndex - 1;
            }
            return true;
        }
    }

    window.addEventListener('load', function (e) {
        $('select.selectfilter').each(function () {
            let $el = $(this), data = $el.data();

            SelectFilter.init($el.attr('id'), data.fieldName, parseInt(data.isStacket, 10));
        });
    });
})(jQuery);
