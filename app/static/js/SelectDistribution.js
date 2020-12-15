(function ($) {
    'use strict';
    function changeState(event) {
				
        if (SelectDistribution.distribution.type == 'Step') {
					SelectDistribution.distribution['cycle'][event.target.name] = event.target.value
				} else {
					SelectDistribution.distribution[event.target.name] = event.target.value
				}
        
        let distribution_field = document.getElementById('id_distribution')
        distribution_field.textContent = JSON.stringify(SelectDistribution.distribution)
    }
    
    function getDistribution() {
        return {
            type: '',
            probability: '',
            form: '',
            scale: '',
            exponential_failure_rate: '',
            initial_failure_rate: '',
            cycle: {
                size: '',
                limit: '',
                value: ''
            }
        }
    }

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

    function inputField(name, type, parent, value) {
        let wrapper = quickElement('div', parent, null, 'class', 'd-flex flex-column');

        let input = quickElement(
            'input', wrapper, null, 'name', name,
            'placeholder', name, 'value', value,
            'style', 'width: 100px;margin-right: 0.5rem', 'type', type
        );
        input.addEventListener('change', function(e) {changeState(e)});

        let helper = quickElement('small', wrapper, null);
        helper.textContent = name.replace('_', ' ');

        return wrapper;
    }

    window.SelectDistribution = {
        cache: {},
        distribution: {},

        init: function (select_id) {
            let distribution = JSON.parse(document.getElementById('distribution').textContent)
            SelectDistribution.distribution = Object.assign(getDistribution(), distribution)
            SelectDistribution.cache[select_id] = [
                {value: 'Exponential', text: 'Exponential', displayed: true},
                {value: 'Probability', text: 'Probability', displayed: true},
                {value: 'Weibull', text: 'Weibull', displayed: true},
                {value: 'Step', text: 'Step', displayed: true},
            ]

            this.redisplay_select(select_id);
            this.redisplay_distribution_fields();

            let select = document.getElementById(select_id);
            select.addEventListener('change', function (e) {
                SelectDistribution.distribution.type = this.value
                SelectDistribution.redisplay_distribution_fields();
            });

        },

        redisplay_distribution_fields: function () {
            let {distribution} = SelectDistribution;
            let wrapper = document.getElementById('distribution_fields')
            wrapper.innerHTML = '';

            if (distribution.type == 'Exponential') {
                inputField(
                    'exponential_failure_rate',
                    'text', wrapper,
                    distribution.exponential_failure_rate
                )
            }
            if (distribution.type == 'Probability') {
                inputField(
                    'probability',
                    'text', wrapper,
                    distribution.probability
                )
            }
            if (distribution.type == 'Weibull') {
                inputField(
                    'form',
                    'text', wrapper,
                    distribution.form
                )
                inputField(
                    'scale',
                    'text', wrapper,
                    distribution.form
                )
            }
            if (distribution.type == 'Step') {
                inputField(
                    'size',
                    'text', wrapper,
                    distribution.cycle.size
                )
                inputField(
                    'limit',
                    'text', wrapper,
                    distribution.cycle.limit
                )
                inputField(
                    'value',
                    'text', wrapper,
                    distribution.cycle.value
                )
                inputField(
                    'initial_failure_rate',
                    'text', wrapper,
                    distribution.initial_failure_rate
                )
            }

        },

        redisplay_select: function (id) {
            // Repopulate HTML select box from cache
            let distribution_type = SelectDistribution.distribution.type;
            let box = document.getElementById(id);
            let node;
            $(box).empty(); // clear all options
            let new_options = box.outerHTML.slice(0, -9); // grab just the opening tag
            let cache = SelectDistribution.cache[id];
            for (let i = 0, j = cache.length; i < j; i++) {
                node = cache[i];
                if (node.displayed) {
                    let selected = distribution_type == node.text
                    let new_option = new Option(node.text, node.value, selected, false);

                    // Shows a tooltip when hovering over the option
                    new_option.setAttribute("title", node.text);
                    new_options += new_option.outerHTML;
                }
            }
            new_options += '</select>';
            box.outerHTML = new_options;
        },
    }

    window.addEventListener('load', function (e) {
        $('select.selectchooser').each(function () {
            let $el = $(this), data = $el.data();
            SelectDistribution.init($el.attr('id'));
        });
    });
})(jQuery);
