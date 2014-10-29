#!/usr/bin/perl
use warnings;
use strict;

while (<>){
	if ($_ =~ m/>(AT[12345CG]G\d{5}.\d) \| .* \| .* \| (chr.):(\d+)-(\d+) (FORWARD|REVERSE)/) {
		#print $_;
		my $strand = $5 eq "FORWARD" ? "+" : "-" ;
		my $end = $4 - $3 + 1;
		print "$1\t$2\ttranscript\t1\t$end\t.\t$strand\t.\t0\tID=$1\n";
	}
}
