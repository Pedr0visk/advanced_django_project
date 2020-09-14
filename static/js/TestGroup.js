(function ($) {
  'use strict';

  function quickElement() {
    'use strict';
    var obj = document.createElement(arguments[0]);
    if (arguments[2]) {
      var textNode = document.createTextNode(arguments[2]);
      obj.appendChild(textNode);
    }
    var len = arguments.length;
    for (var i = 3; i < len; i += 2) {
      obj.setAttribute(arguments[i], arguments[i + 1]);
    }
    arguments[1].appendChild(obj);
    return obj;
  }

  window.TestInput = {
    count: 0,
    init: function () {
      $('input.testcoverage').each(function () {
        console.log('log log')
        this.addEventListener('blur', e => on_blur(this));
        TestInput.count++
      });

      let wrapper = document.getElementById('testsWrapper')
      let add_link = document.getElementById('addLevelBtn');

      add_link.addEventListener('click', function (e) {
        add_test_level(wrapper);
      });

      function add_test_level(node) {
        TestInput.count++

        if (TestInput.count > 4) {
          enable_add_field(false)
          return
        };

        let form_row = document.createElement('div')
        let hr = document.createElement('hr')
        let label = document.createElement('label')
        let colum_1 = document.createElement('div')
        let colum_2 = document.createElement('div')

        let interval_input = document.createElement('input')
        let coverage_input = document.createElement('input')

        colum_1.appendChild(interval_input)
        colum_2.appendChild(coverage_input)

        form_row.classList = ['form-group row px-3']
        label.classList = ['col-sm-2 col-form-label col-form-label-sm']
        label.textContent = 'test level ' + TestInput.count

        interval_input.classList = ['form-control form-control-sm']
        coverage_input.classList = ['form-control form-control-sm testcoverage']
        coverage_input.setAttribute('data-level', TestInput.count)
        let c_id = 'coverage_' + TestInput.count
        coverage_input.id = c_id

        colum_1.classList = ['col-sm-1']
        colum_2.classList = ['col-sm-1']


        node.appendChild(form_row)
        form_row.appendChild(label)
        form_row.appendChild(colum_1)
        form_row.appendChild(colum_2)
        node.appendChild(hr)

        document.getElementById(c_id).addEventListener('blur', function (e) {
          on_blur(this)
        })
      }

      function remove_test_levels(node) {
        let currentLevel = node.dataset.level;

        $('input.testcoverage').each(function () {
          if (this.dataset.level > currentLevel) {
            let elem = findForm(this)
            wrapper.removeChild(elem.nextSibling);
            wrapper.removeChild(elem);
            TestInput.count--
          }
        });
      }

      function findForm(node) {
        // returns the node of the form containing the given node
        if (!node.classList.contains('form-group')) {
          return findForm(node.parentNode);
        }
        return node;
      }

      function on_blur(node) {
        enable_add_field(node.value < 1)
        if (node.value >= 1) {
          remove_test_levels(node)
        }
      }

      function enable_add_field(status) {
        if (status) {
          add_link.removeAttribute('disabled')
        } else {
          add_link.setAttribute('disabled', status)
        }
      }
    },
  }

  function _getIntervalElem(elem) {
    return elem.parentNode.previousElementSibling.firstElementChild
  }

  window.addEventListener('load', function (e) {
    setTimeout(function() {
      console.log('iniciado')
      TestInput.init();
      $('input.testcoverage').each(function () {
        console.log('log log')
      });
    }, 2000)

    // OnSubmit Event Handler
    document.getElementById('testGroup').addEventListener('submit', function (e) {
      let data = [];

      $('input.testcoverage').each(function () {
        data.push({ coverage: this.value, interval: _getIntervalElem(this).value })
      });

      this.tests.value = JSON.stringify(data);
    });
  });


})(jQuery);
