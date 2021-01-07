class NotificationObj {
  constructor(notificationObj) {
    this.notificationObj = notificationObj
  }

  creationReminder() {
    var reminder = `
      <div aria-live="polite" aria-atomic="true" style="position: relative;">
        <div id="toast" class="toast" data-delay="5000" style="position: absolute; top: 0; right: 10px;">
          <div class="toast-header">
            <img src="/static/img/icon-yes.svg" class="rounded mr-2" alt="...">
            <strong class="mr-auto">Notification </strong>
            <small class="ml-2">${this.getDate()}</small>
            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="toast-body">
            ${this.notificationObj.body}
          </div>
        </div>
      </div>
    `
    return reminder;
  }

  getDate() {
    let milleseconds = Date.now() - new Date(this.notificationObj.creation_date);
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