#!/usr/bin/perl
use strict;
use warnings;
use Bio::DB::GenBank;
use Bio::DB::FileCache;
use Bio::DB::GenPept;
use Bio::Seq;
use Bio::DB::EUtilities;


my $ntdb 	= Bio::DB::GenBank->new(-delay=>1);
my $cachent 	= new Bio::DB::FileCache(-kept => 1,
					-file => '/tmp/nt.idx',
					-seqdb => $ntdb);

my $pepdb 		= Bio::DB::GenPept->new(-delay=>1);
my $cachepep	= new Bio::DB::FileCache(-kept => 1,
					-file => '/tmp/pep.idx',
					-seqdb => $pepdb);
						
my @protAccessionList 	= qw(AAF97287.1 AAF97288.1 AAF97279.1 AAF97294.1 AAF97281.1 AAF97283.1 AAF97282.1 AAF97292.1 AAF97280.1 AAF97296.1 NP_201203.2 AAG40733.1 AAG40732.1 AAG40731.1 NP_568970.2);
sub joinParts($)
{
	my ($joinString)	=	@_;
	my @parts			=	split(/,/,$joinString);
	my $seqPlainText	=	'';
	foreach my $thisPart (@parts)
	{
		if($thisPart =~ m/:/)
		{
			my ($accession,$location)	=	split(/:/,$thisPart);
			my ($start,$end)			=	0;
			($start,$end)				=	split(/\.\./,$location);
			print ("getting seq: $accession from $start to $end should be " . (($end - $start)+1) . " bp long\n");
			my $efetchObj 				=	Bio::DB::EUtilities->new(
											-eutil		=> 'efetch',
											-db			=> 'nucleotide',
											-rettype	=> 'fasta',
											-email  	=> 'u4852380@anu.edu,au',
											-seq_start	=> "$start",
											-seq_stop	=> "$end",
											-id			=> "$accession"
											);
			my $returnedObj				=	$efetchObj->get_Response->content;
			my @fastaFile				=	split(/\n/,$returnedObj);
			#print(join("\n" ,@fastaFile) . "\n\n");
			my $thisPartSeqPT;
			foreach my $fastaLine (@fastaFile)
			{
				next if($fastaLine =~ m/>/);
				chomp $fastaLine;
				$thisPartSeqPT	.=	$fastaLine;
			}
			$seqPlainText .= $thisPartSeqPT;
			print ("was " . length ($thisPartSeqPT) . " bp long\n");
		}
		else
		{
			#use current seqobj. not implemented
		}
	}
	return $seqPlainText;
}
sub getCodedBySeq($)
{
	my ($codedBy) 		=	@_;
	my $commandString  	=	$codedBy;
	my $seqPlainText	=	'';
	my $strand			=	1;
	if($commandString =~ m/[\(\)]/)
	{
		while($commandString =~ m/[\(\)]/)
		{
#			print ("command String is $commandString \n");
			#get the command, and the stuff inside the brackets (called arguments here, may contain other strings
			my($command, $arguments) = split(/\(/,$commandString,2);
			$arguments =~ s/\)$//;
#			print ("command is $command, args are $arguments\n");
			if($command eq "join")
			{
				$commandString  = 	$arguments;
				$seqPlainText	=	joinParts($arguments);
			}
			elsif($command eq "complement")
			{
				$commandString  = 	$arguments;
				$strand			=	2;
			}
		}
	}
	else
	{
		$seqPlainText	=	joinParts($commandString);
	}
	if($strand ==1)
	{
		return $seqPlainText;
	}
	else
	{
		my $seqObj	=	Bio::Seq->new(-seq => $seqPlainText);
		return $seqObj->revcom->seq;
	}
}
foreach my $protAccession (@protAccessionList)
{
	my $nucAccession;
	my $nucSeqobj;
	my $nucSeq;
	my $protSeq = $cachepep->get_Seq_by_acc($protAccession);
	if (!$protSeq) {warn("No sequence found for protein accession $protAccession, skipping it\n");next;}
	foreach my $cdsSeqFeatureObj (  grep { $_->primary_tag eq 'CDS' } $protSeq->get_SeqFeatures())
	{
		next unless( $cdsSeqFeatureObj->has_tag('coded_by') ); # skip CDSes with no coded_by
		my ($codedby)			=	$cdsSeqFeatureObj->each_tag_value('coded_by');
		$nucSeq					=	getCodedBySeq($codedby);
		my $len					=	length($nucSeq);
	}
}
