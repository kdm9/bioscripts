function _ymdToISO(y, m, d){
  date = new Date(y, m, d);
  datestr = date.getFullYear().toString()
  datestr += "-" + ("0" + (date.getMonth() + 1).toString()).slice(-2)
  datestr += "-" + ("0" + (date.getDate() + 1).toString()).slice(-2)
  return(datestr);
}

function ausDateToISO(date) {
  split = date.split("/");
  [d, m, y] = split;
  return(_ymdToISO(y,m,d))
}

function usDateToISO(date) {
  split = date.split("/");
  [m, d, y] = split;
  return(_ymdToISO(y,m,d))
}
