/* Pattern declarations */
var r_degminsecdir = /^\s*(\d+)[°º\*]\s*(\d+)'\s*(\d+.?\d*)\"\s*([NnSsWwEe])\s*$/;
var r_dirdegminsec = /^\s*([NnSsWwEe])\s*(\d+)[°º\*]\s*(\d+)'\s*(\d+.?\d*)\"\s*$/;
var r_dirdecimal = /^\s*([NnSsWwEe])\s*(\d+\.?\d*)\s*$/;
var r_decimaldir = /^\s*(\d+\.?\d*)\s*([NnSsWwEe])\s*$/;
var r_decimal = /^\s*(-?\d+\.?\d*)\s*$/;

/* Helper functions */
function dms2dec(deg, min, sec, dir){
  dec = parseFloat(deg) + (parseFloat(min) / 60.0) + (parseFloat(sec) / 3600.0);
  dec *= parseFloat(dir);
  return dec;
}

function dir2num(dir){
  dir = dir.toUpperCase()
  return (dir == "N" || dir == "E") ? 1.0 : -1.0;
}


/* actual fucntion */

function convLatLon(initial){
  /* takes a string in any format supported by regex above */
  /*initial="37° 46' 14.5\"N"*/

  /*avoid "Too many simulaneous scripts for this user" error*/
  Utilities.sleep(Math.random() * 10000);

  if (initial == "" || initial == null){
    return(null)
  }
  else if (r_degminsecdir.test(initial)){
    split = r_degminsecdir.exec(initial);
    [_, deg, min, sec, dir] = split;
    dir = dir2num(dir);
    return(dms2dec(deg, min, sec, dir))
  }
  else if (r_dirdegminsec.test(initial)){
    split = r_dirdegminsec.exec(initial);
    [_, dir, deg, min, sec] = split;
    dir = dir2num(dir);
    return(dms2dec(deg, min, sec, dir))
  }
  else if (r_decimal.test(initial)){
    split = r_decimal.exec(initial);
    [_, dec] = split;
    return(parseFloat(dec));
  }
  else if (r_decimaldir.test(initial)){
    split = r_decimaldir.exec(initial);
    [_, dec, dir] = split;
    return(parseFloat(dec) * dir2num(dir));
  }
  else if (r_dirdecimal.test(initial)){
    split = r_dirdecimal.exec(initial);
    [_, dir, dec] = split;
    return(parseFloat(dec) * dir2num(dir));
  }
  else
  {
    return("INVALID")
  }

}
