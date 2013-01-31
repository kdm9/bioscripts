#!/usr/bin/perl
use strict;
use warnings;
use Tie::Handle::CSV;
use Bio::Seq;
use Getopt::Long;

my $infile 		= 	'';
my $outfile		=	'';
my $verbose 	=	0;

my $getoptResult	= 	GetOptions(
						'verbose+'	=>	\$verbose,
						'infile=s'	=>	\$infile,
						'outfile=s'	=>	\$outfile
						);

if(!$getoptResult)
{die("bad getopt result");}

if(! -e $infile )
{die("Input file required\n");}

if (!$outfile)
{
	my @filenamesplit = split(/\./,"$infile") ;
	$outfile = $filenamesplit[0];
}

my $outfileF	=	"$outfile.FWD.csv";
my $outfileR	=	"$outfile.REV.csv";
if(-e $outfileR )
{
	if($verbose > 0)
	{verb("Deleting old output file: $outfileR\n");}
	unlink($outfile);
}

if(-e $outfileF )
{
	if($verbose > 0)
	{verb("Deleting old output file: $outfileF\n");}
	unlink($outfile);
}
my $inputCSVFH = Tie::Handle::CSV->new("$infile",header=>1);

open(FPRIMERS,">$outfileF");
print FPRIMERS ("\"Well\",\"OligoName\",\"OligoSequence\",\"Notes\"\n");
close FPRIMERS;

open(RPRIMERS,">$outfileR");
print RPRIMERS ("\"Well\",\"OligoName\",\"OligoSequence\",\"Notes\"\n");
close RPRIMERS;

while(my $csvline = <$inputCSVFH>) 
{
    if ($csvline->{'5PrimerATT'} && $csvline->{'3PrimerATT'})
    {
		my $truncationStart 	=	$csvline->{'TruncStart'} 	? "From " . $csvline->{'TruncStart'}	: "From Start"; ;
		my $truncationEnd 		=	$csvline->{'TruncEnd'} 		? "To " . $csvline->{'TruncEnd'}		: "To End";
		
		my $thisFPrimer 		=	$csvline->{'5PrimerATT'};
		my $thisFPrimerName 	= 	$csvline->{'ShortName'} . "_" . $csvline->{'Truncation'} . "_FOR";
		my $thisFPrimerNotes 	= 	$csvline->{'Protein'} . "_$truncationStart $truncationEnd _" . $csvline->{'ProtAccession'};
	
		open(FPRIMERS,">>$outfileF");
		print FPRIMERS ("\"". $csvline->{'Well Number'} ."\",\"$thisFPrimerName\",\"$thisFPrimer\",\"$thisFPrimerNotes\"\n");
		close FPRIMERS;
		
		my $thisRPrimer			= 	$csvline->{'3PrimerATT'};
		my $thisRPrimerName 	=	$csvline->{'ShortName'} . "_" . $csvline->{'Truncation'} ."_REV";
		my $thisRPrimerNotes 	=	$csvline->{'ProtAccession'} . "_$truncationStart $truncationEnd _" . $csvline->{'Protein'};
		
		open(RPRIMERS,">>$outfileR");
		print RPRIMERS ("\"". $csvline->{'Well Number'} ."\",\"$thisRPrimerName\",\"$thisRPrimer\",\"$thisRPrimerNotes\"\n");
		close RPRIMERS;
    }
    else
    {
    	my $thisFPrimer 		= 	"Empty";
		my $thisFPrimerName 	= 	$csvline->{'ShortName'} ."_FOR";
		my $thisFPrimerNotes 	= 	"EMPTY WELL " . $csvline->{'Protein'};
		open(FPRIMERS,">>$outfileF");
		print FPRIMERS ("\"". $csvline->{'Well Number'} ."\",\"$thisFPrimerName\",\"$thisFPrimer\",\"$thisFPrimerNotes\"\n");
		close FPRIMERS;
		
		my $thisRPrimer 		= 	"Empty";
		my $thisRPrimerName 	= 	$csvline->{'ShortName'} ."_REV";
		my $thisRPrimerNotes 	= 	"EMPTY WELL " . $csvline->{'Protein'};
		open(RPRIMERS,">>$outfileR");
		print RPRIMERS ("\"". $csvline->{'Well Number'} ."\",\"$thisRPrimerName\",\"$thisRPrimer\",\"$thisRPrimerNotes\"\n");
		close RPRIMERS;
	}
}
close $inputCSVFH;
