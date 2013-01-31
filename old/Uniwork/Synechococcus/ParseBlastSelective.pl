#!/usr/bin/perl
use warnings;
use Bio::DB::RefSeq;
use Bio::DB::GenBank;
use Bio::DB::EMBL;
use Bio::SearchIO;
my $usegenus = 0;
my $makeCSV = 1;
my $makeFasta = 1;
my $makeList = 0;

my @strains;
my @genuses;
my $IdentityCutoff = 30;
my $HomologyCutoff = 80;
my $SizeCutoff = 80;
#my $
$inputfile = shift;
my $in = new Bio::SearchIO(-format => 'blastxml', -file => "$inputfile", -verbose => 1);
my $outfilename = $inputfile;
open(CSVHEADERFILE,">$outfilename"  . ".csv");
print CSVHEADERFILE ("Strain,accession,gi number,Sequence,Description,Expect,Identity,Conserved,Gaps,HitLength,HitLengthAsPercentOfGene\n");
close CSVHEADERFILE;


while (my $result = $in->next_result){
	while (my $hit = $result->next_hit)
	{
		my $thisHSP = $hit->hsp('best');
		my $desc =  $hit->description;


		@splitdesc = split('>', $desc);
		$desc = $splitdesc[0];

		$desc =~ s/\n//g;
		$desc =~ s/\]//g;
		my @nametokens = split('\[', $desc);
		my $strainname = $nametokens[1];
		my $genus = $nametokens[1];

		$strainname ||='XXXXX NO NAME XXXXX';
		if ($strainname eq 'XXXXX NO NAME XXXXX'){next;}
		$strainname =~ s/\]//g;#remove trailing ]
		$strainname =~ s/^\s+//;#remove leading space
		$strainname =~ s/\s+$//;#remove trailing sp
		$strainname =~ s/\s+/-/g;#convert remaining spaces to -

		$genus ||='XXXXX NO NAME XXXXX';
		if ($genus eq 'XXXXX NO NAME XXXXX'){next;}
		$genus =~ s/\]//g;#remove trailing ]
		$genus =~ s/^\s+//;#remove leading space
		$genus =~ s/\s+$//;#remove trailing sp
		@genussplit = split("\ ", $genus);
		$genus = $genussplit[0];# . " " . $genussplit[1];
		$genus =~ s/\s+/-/g;#convert remaining spaces to -
		if($usegenus) {$strainname = $genus;}
		if($usegenus)
		{
			%genushash = map { $_ => 1 } @genuses;
			if (!$genushash{$genus})
			{
				push(@genuses, $genus);
				#print($strainname, "\n");
				my $identifier = $hit->name;
				my @idSplit = split(/\|/, $identifier);
				$identifier = $idSplit[1];
				my $dbobj = Bio::DB::GenBank->new( -delay => 1);
				#my $seqobj = $dbobj->get_Seq_by_acc($hit->accession);
				my $seqobj = $dbobj->get_Seq_by_gi($identifier);
				open(OUTFILE,">>$outfilename" . ".fasta");
				print OUTFILE (">", $genus, "\n", $seqobj->seq, "\n\n");
				print(">", $genus, "\n", $seqobj->seq, "\n\n");
				close OUTFILE;
			}
		}
		else
		{
			eval {%strainhash = map { $_ => 1 } @strains;};  warn $@ if $@;
			if (!$strainhash{$strainname})
			{
				my $seqobj;
				my $dbobj;
				push(@strains, $strainname);
				#print($strainname, "\n");
				my $identifier = $hit->name;
				my @idSplit = split(/\|/, $identifier);
				$identifier = $idSplit[1];

				$dbobj = Bio::DB::GenBank->new( -delay => 0);
				eval
				{
					$seqobj = $dbobj->get_Seq_by_gi($identifier);
					my $subjectLength = 0;
				};
				if ($@)
				{
					next;
				}
				
				my $HitDesc = $desc;
				my $thisHomology = 0;
				my $thisSize = 0;
				my $hspIdentity = 0;
				my $hspConserved = 0;
				my $hspGaps = 0;
				my $hspLengthOfHomology = 0;
				my $hspPercentOverlap = 0;
				
				if ($thisHSP)
				{
					$hspIdentity = $thisHSP->frac_identical('total');
					$hspIdentity =int(($hspIdentity * 1000) + 0.5) / 10;
					
					$hspConserved = $thisHSP->frac_conserved('total');
					$hspConserved =int(($hspConserved * 1000) + 0.5) / 10;
					
					$hspLengthOfHomology = $thisHSP->length('total');
					
					$hspGaps = $thisHSP->gaps();
					$hspGaps = int((($hspGaps/$hspLengthOfHomology) * 1000) + 0.5) / 10;
					
					$hspPercentOverlap = int((($hspLengthOfHomology/$seqobj->length) * 1000) + 0.5) / 10;
					
					#$infoString = $HitDesc . "\t Percent Identity: " . $hspIdentity . " \tPercent Conserved: " . $hspConserved . " \tGaps: " .  $hspGaps . "\t Hit Overlap Length: " . $hspLengthOfHomology . " \tHomology as Percentage of Subject Length: " . $hspPercentOverlap . "\n";
					
					$thisHomology = $hspLengthOfHomology;
					$thisHomology /= $result->query_length;
					$thisHomology = int((($thisHomology) * 1000) + 0.5) / 10;

					$thisSize = $hspLengthOfHomology / $seqobj->length;
					$thisSize = int((($thisSize) * 1000) + 0.5) / 10;
					
					if ($hspIdentity < $IdentityCutoff) {print "Low Identity: " . $hspIdentity . "\n"; next;}
					if ($thisHomology < $HomologyCutoff) {print "Low Homology: " . $thisHomology . "\n";next;}
					if ($thisSize < $SizeCutoff) {print "Low Size: " . $thisSize . "\n";next;}
				}
				
				if($makeFasta)
				{
					open(OUTFILE,">>$outfilename" . ".fasta");
					print OUTFILE (">", $strainname, " " ,$HitDesc , "\n" , $seqobj->seq, "\n\n");
					print(">", $strainname,"\n");
					close OUTFILE;
				}
				if ($makeList)
				{
					
					open(LISTFILE,">>$outfilename" . ".list");
					print LISTFILE ($strainname, "\n##########################\n# ", $HitDesc,  "\n# Percent Identity: " . $hspIdentity . "\n# Percent Conserved: " . $hspConserved . "\n# Gaps: " .  $hspGaps . "\n# Hit Overlap Length: " . $hspLengthOfHomology . " \n# Homology as Percentage of Subject Length: " . $hspPercentOverlap . "\n\n\n");
					close LISTFILE;
				}
				if ($makeCSV)
				{
					$HitDesc =~ s/,//g;
					$strainname =~ s/,//g;
					open(CSVFILE,">>$outfilename" . ".csv");
					print CSVFILE (join(",",$strainname,$hit->accession,$identifier, $seqobj->seq,$HitDesc,$thisHSP->expect(),$hspIdentity, $hspConserved, $hspGaps, $hspLengthOfHomology , $hspPercentOverlap),"\n");
					close CSVFILE;
				}
			}
		}
	}
}

