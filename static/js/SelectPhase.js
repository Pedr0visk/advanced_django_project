(function ($) {
    'use strict';

    function quickElement() {
        let obj = document.createElement(arguments[0]);
        if (arguments[2]) {
            let textNode = document.createTextNode(arguments[2]);
            obj.appendChild(textNode);
        }
        let len = arguments.length;
        for (let i = 3; i < len; i += 2) {
            obj.setAttribute(arguments[i], arguments[i + 1]);
        }
        arguments[1].appendChild(obj);
        return obj;
    }

    function _setOptionsToSelect(box, options) {
        let node;
        let new_options = box.outerHTML.slice(0, -9);
        for (let i = 0, j = options.length; i < j; i++) {
            node = options[i];
            let new_option = new Option(node.text, node.value, false, false);
            // Shows a tooltip when hovering over the option
            new_option.setAttribute("title", node.text);
            new_options += new_option.outerHTML;
        }
        new_options += '</select>';
        box.outerHTML = new_options;
    }

    const SelectPhase = {
        index: 1,
        cache: {},
        classes: 'form-control form-control-sm',
        steps: [
            {value: 1, text: 'descend'},
            {value: 2, text: 'connect'},
            {value: 3, text: 'drilling'},
            {value: 4, text: 'disconnect'},
            {value: 5, text: 'test'}
        ],
        groups: [],

        init: async function (field_id) {
            let bopId = $('#bopId').val();
            const response = await fetch(`/api/bops/${bopId}/test-groups`);
            const data = await response.json();
            this.groups = data.testgroup.map(g => ({value: g, text: `test group ${g}`}))
            SelectPhase.load_table_input(field_id);
        },
        load_table_input: function (field_id) {
            let node = document.getElementById(field_id);
            let tr = quickElement('tr', node);

            // field name
            let td = quickElement('td', tr);
            quickElement('input', td, null, 'placeholder',
                'name', 'class', this.classes, 'id', 'phaseName');

            // field start_date
            td = quickElement('td', tr);
            quickElement('input', td, null, 'class', this.classes,
                'type', 'datetime-local', 'id', 'date');

            // field duration
            td = quickElement('td', tr);
            quickElement('input', td, null, 'placeholder', 'duration',
                'class', this.classes, 'type', 'number', 'id', 'duration');

            // field step
            td = quickElement('td', tr);
            let stepSelector = quickElement('select', td, null, 'class',
                this.classes, 'id', 'step');
            _setOptionsToSelect(stepSelector, this.steps);

            document.getElementById('step').addEventListener('change', function (e) {
                let selector = document.getElementById('testGroup');
                if (this.value == 5) {
                    selector.classList.remove('d-none')
                } else {
                    selector.classList.add('d-none')
                }
            });

            // field test group
            td = quickElement('td', tr);
            let testGroupSelector = quickElement('select', td, null, 'class',
                this.classes + ' d-none', 'id', 'testGroup', 'multiple');

            _setOptionsToSelect(testGroupSelector, this.groups)

            td = quickElement('td', tr);
            let addBtn = quickElement('button', td, 'add', 'class',
                'btn btn-standard', 'id', 'add');
            addBtn.addEventListener('click', function (e) {
                e.preventDefault();
                SelectPhase.add_to_cache(e, field_id);
            });
        },
        redisplay: function (field_id) {
            let cache = SelectPhase.cache;
            let node = document.getElementById(field_id);
            $(node).empty();

            for (let key in cache) {
                let tr = quickElement('tr', node);
                let obj = cache[key];

                // saved data
                for (let attr in obj) {
                    let td = quickElement('td', tr),
                        config = [
                            'input', td, null,
                            'value', obj[attr],
                            'class', this.classes,
                            'disabled', true
                        ];
                    let $el = quickElement(...config);
                }
            }

            SelectPhase.load_table_input(field_id);
        },
        add_to_cache: function (e, field_id) {
            let name = $('#phaseName').val(),
                start_date = $('#date').val(),
                duration = $('#duration').val(),
                step = $('#step').val(),
                test_groups = $('#testGroup').val();

            let id = this.index;
            SelectPhase.cache[id] = {name, start_date, duration, step, test_groups}
            SelectPhase.redisplay(field_id);
            this.index++;
        },
    };

    window.SelectPhase = SelectPhase

    window.addEventListener('load', function (e) {
        SelectPhase.init('phases_list');

        $('#campaignForm').on('submit', async function (e) {
            e.preventDefault();
            let data = {};

            data.name = this.name.value;
            data.well_name = this.well_name.value;
            data.description = this.description.value;
            data.bop = this.bop.value;
            data.active = this.active.value;
            data.start_date = this.start_date.value;
            data.end_date = this.end_date.value;

            let phases = Object.values(SelectPhase.cache)
            data.phases = phases;

            let content = await createCampaign(data);
            if (content.status == 201) {
                alert('Campaign Successfully created! Go to campaign pages.')
            }
        });


        async function createCampaign(data) {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const rawResponse = await fetch('/api/campaigns/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                mode: 'same-origin',
                body: JSON.stringify(data)
            })

            return rawResponse;
        }
    });
})(jQuery)
