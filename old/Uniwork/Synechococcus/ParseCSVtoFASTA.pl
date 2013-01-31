#!/usr/bin/perl
use warnings;
use Tie::Handle::CSV;
my $makeFasta = 1;
my $makeList = 0;

$inputfile = shift;
my $csvFH = Tie::Handle::CSV->new("$inputfile",header=>1);
@split = split(/\./,"$inputfile") ;
my $outfilename = $split[0];

while(my $csvline = <$csvFH>) {
    if ($csvline->{'Use'})
    {
	open(OUTFILE,">>$outfilename" . ".fasta");
	print OUTFILE (">", $csvline->{'Strain'}, " " , $csvline->{'gi number'} , " " , $csvline->{'Description'} ,"\n", $csvline->{'Sequence'}, "\n\n");
	print ( $csvline->{'Strain'},"\n");
	close OUTFILE;
    }   
}

close $csvFH;