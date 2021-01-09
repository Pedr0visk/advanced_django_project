import Vue from 'vue';

const calcDateTime = function (date, time, delay) {
  let tmp = (parseInt(delay) + parseInt(time)) * 60 ** 2 * 1000
  let new_date = new Date(new Date(date.split('-')).getTime() + tmp)
  return new_date;
}

const toDateString = function (date) {
  return `${date.getFullYear()}-${("0" + (date.getMonth() + 1)).slice(-2)}-${("0" + (date.getDate())).slice(-2)}`
}

const formatDate = function(date, hour) {
  if (!date) return;

  let d = new Date(date.split('-')),
    month = '' + (d.getMonth() + 1),
    day = '' + d.getDate(),
    year = d.getFullYear();

  if (month.length < 2)
    month = '0' + month;
  if (day.length < 2)
    day = '0' + day;

  return `${[year, month, day].join('-')} ${("0" + hour).slice(-2)}:00:00`;
}

export default {
  install: () => {
    Vue.prototype.calcDateTime = calcDateTime
    Vue.calcDateTime = calcDateTime

    Vue.prototype.formatDate = formatDate
    Vue.formatDate = formatDate

    Vue.prototype.toDateString = toDateString
    Vue.toDateString = toDateString
  }
}

