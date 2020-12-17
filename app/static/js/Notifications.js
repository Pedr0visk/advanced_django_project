(function ($) {
  'use strict';

  class Toast {
    constructor(notificationObj) {
      this.notificationObj = notificationObj
    }

    creationReminder() {
      var reminder = `
        <div aria-live="polite" aria-atomic="true" style="position: relative; min-height: 200px;">
          <div class="toast" data-delay="7000" style="position: absolute; top: 0; right: 10px;">
            <div class="toast-header">
              <img src="/static/img/icon-yes.svg" class="rounded mr-2" alt="...">
              <strong class="mr-auto">Notification </strong>
              <small class="ml-2">${this.getDate()}</small>
              <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="toast-body">
              ${this.notificationObj.fields.body}
            </div>
          </div>
        </div>
      `
      return reminder;
    }

    getDate() {
      let milleseconds = Date.now() - new Date(this.notificationObj.fields.creation_date);
      let seconds = milleseconds / 3600;
      if (seconds < 60) {
        return parseInt(seconds, 10) + 's ago'
      }
      return parseInt(milleseconds / 3600, 10);
    }

    drawNotification() {
      if (this.notificationObj.group === 'c') return this.creationReminder();
      return this.creationReminder();
    }
  }

  window.Notification = {
    init: function (userId) {

      const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/notifications/'
        + userId
        + '/'
      );

      chatSocket.onmessage = async function (e) {
        const data = JSON.parse(e.data);
        let unreadNotifications = JSON.parse(data.unreaded_notifications)

        unreadNotifications.map(notification => {
          if (notification.fields.group == 'c') {
            let btn = document.getElementById('btnCompare');
            let img = document.createElement('img');
            let text = document.createElement('small');

            btn.textContent = '';
            btn.classList = 'btn btn-success';
            btn.style = 'cursor: not-allowed';

            img.src = '/static/img/loading.gif';
            img.width = '15';
            btn.appendChild(img);

            text.textContent = 'COMPARING SCHEMAS...';
            btn.appendChild(text);

            $('#task_alert').addClass('d-flex')
          }

          if (notification.fields.group == 'd') {
            let btn = document.getElementById('btnCompare');
            let text = document.createElement('small');

            btn.textContent = '';
            btn.style = '';
            btn.classList = 'btn btn-primary';

            text.textContent = 'SEE SCHEMAS COMPARISON';
            btn.appendChild(text);

            $('#task_alert').removeClass('d-flex')
          }

          // Notification.createNotification(notification);
        });

        $('.toast').toast('show');
      };

      chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
      };
    },

    createNotification(data) {
      console.log(data)
      let content = document.getElementById('notifications_content');
      let toast = new Toast(data);

      content.innerHTML = toast.drawNotification();
    }

  }

  window.addEventListener('load', function (e) {
    const userId = JSON.parse(document.getElementById('userId').textContent);
    console.log('user id', userId)
    Notification.init(userId);
  });
})(jQuery);
