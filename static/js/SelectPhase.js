(function ($) {
    'use strict';

    const SelectPhase = {
        index: 1,
        cache: {},

        init: function (field_id) {
            let addBtn = document.getElementById('add');

            addBtn.addEventListener('click', function (e) {
                e.preventDefault();
                SelectPhase.add_to_cache(e, field_id);
            })
        },
        redisplay: function () {
            /**
             * this function should get all phases added and list
             */
        },

        add_to_cache: function (e, elem_id) {
            let name = $('#name').val(),
                date = $('#date').val(),
                duration = $('#duration').val(),
                step = $('#step')

            let id = 1;
            SelectPhase.cache[id].push({name, date, duration, step});
            console.log(SelectPhase.cache);
        },

        add_new_phase: function (e, elem_id) {
        },
    };

    window.SelectPhase = SelectPhase

    window.addEventListener('load', function (e) {
        SelectPhase.init('phaseFieldSet')
    });
})(jQuery)
