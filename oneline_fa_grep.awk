#!/usr/bin/awk -f

BEGIN{
	RS=">";
	FS="\n";
}
NR>1{
	hdr=$1
	rec="";
	for (i=2; i<=NF; i++) {
		print($i);
		rec += gsub(/\n/, "", $i);
	}
	printf(">%s\n%s\n", $hdr, $rec);
}
