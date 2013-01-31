#!/usr/bin/perl
use strict;
use warnings;
use Tie::Handle::CSV;
use IPC::Open3;
use Getopt::Long;
use Bio::DB::GenBank;
use Bio::DB::FileCache;
use Bio::DB::GenPept;
use Bio::Seq;
use Bio::DB::EUtilities;

my $infile       =     '';
my $outfile      =    '';
my $oligotm      =    '';
my $verbose      =    0;
my $fATT         =     "GGGGACAAGTTTGTACAAAAAAGCAGGCTTCGGTACC";
my $rATT         =     "GGGGACCACTTTGTACAAGAAAGCTGGGTGACTAGT";
my $getoptResult    =     GetOptions(
                        'verbose+'  =>    \$verbose,
                        'infile=s'  =>    \$infile,
                        'outfile=s' =>    \$outfile,
                        'oligotm=s' =>    \$oligotm,
                        'fatt=s'    =>    \$fATT,
                        'ratt=s'    =>    \$rATT,
                        );


if(!$getoptResult)
{die("bad getopt result");}

if(! -e $infile )
{die("Input file required\n");}

if (!$outfile)
{
    my @filenamesplit = split(/\./,"$infile") ;
    $outfile = $filenamesplit[0] . "_processed.csv";
}

if(-e $outfile )
{
    if($verbose > 0)
    {verb("Deleting old output file: $outfile\n");}
    unlink($outfile);
}

if(!$oligotm)
{
    $oligotm = "oligotm";
}

if($fATT)
{
    if($fATT =~ m/[^GgCcAaTt]/)
    {$fATT     =     "GGGGACAAGTTTGTACAAAAAAGCAGGCTTCGGTACC"};
}
else
{$fATT         =     "GGGGACAAGTTTGTACAAAAAAGCAGGCTTCGGTACC"}

if($rATT)
{
    if($rATT =~ m/[^GgCcAaTt]/)
    {$rATT     =     "GGGGACCACTTTGTACAAGAAAGCTGGGTGACTAGT"};
}
else
{$rATT         =     "GGGGACCACTTTGTACAAGAAAGCTGGGTGACTAGT"}

my $csvFH = Tie::Handle::CSV->new("$infile",header=>1);
if (!$csvFH)
{die("Could not create CSV filehandle");}

my $genbankDBObj    = Bio::DB::GenBank->new(-delay=>2);
my $genbankCacheObj = new Bio::DB::FileCache(-kept => 1,
                        -file => '/tmp/nt.idx',
                        -seqdb => $genbankDBObj);
my $genpeptDBObj    = Bio::DB::GenPept->new(-delay=>2);
my $genpeptCacheObj = new Bio::DB::FileCache(-kept => 1,
                        -file => '/tmp/pep.idx',
                        -seqdb => $genpeptDBObj);

sub joinParts($)
{
    my ($joinString)     =    @_;
    my @parts            =    split(/,/,$joinString);
    my ($nucAccession,$seqPlainText) = '';

    foreach my $thisPart (@parts)
    {
        # chomp ($thisPart);
        # $thisPart =~ s/^\s+//;
        # $thisPart =~ s/\s+$//;
        my $strand    =    1;
        
        #handle revcom specification
        if($thisPart =~ m/[\)\)]/)
        {    
            my($command, $arguments) = split(/\(/,$thisPart,2);
            $arguments =~ s/\)$//;
            
            if(grep(/complement/,$command))
            {
                $thisPart          =     $arguments;
                $strand            =    2;
            }
        }
        
        
        if($thisPart =~ m/:/)
        {
            my $thisPartSeqPT;
            my ($start,$end)           =    0;
            my ($accession,$location)  =    '';
            my $efetchObj;
            
            ($accession,$location)     =    split(/:/,$thisPart);
            ($start,$end)              =    split(/\.\./,$location);
            
            eval
            {
                $efetchObj             =    Bio::DB::EUtilities->new(
                                            -eutil      => 'efetch',
                                            -db         => 'nucleotide',
                                            -rettype    => 'fasta',
                                            -email      => 'u4852380@anu.edu,au',
                                            -seq_start  => "$start",
                                            -seq_stop   => "$end",
                                            -id         => "$accession"
                                            );
            } or do {warn("\tCould not EFetch nucleotide accession $accession, skipping it\n". join('__',@_));return (undef,undef);};
            
            eval {$efetchObj->get_Response}
            or do {warn("\tEFetch of nucleotide accession $accession returned invalid result or error\n");return (undef,undef);};
            
            my $returnedObj            =    $efetchObj->get_Response->content;
            my @fastaFile              =    split(/\n/,$returnedObj);
            #print(join("\n" ,@fastaFile) . "\n\n");
            
            foreach my $fastaLine (@fastaFile)
            {
                next if($fastaLine =~ m/>/);
                chomp $fastaLine;
                $thisPartSeqPT        .=    $fastaLine;
            }
            
            if($strand !=1)
            {
                my $seqObj            =    Bio::Seq->new(-seq => $thisPartSeqPT);
                $thisPartSeqPT        =     $seqObj->revcom->seq;
            }
            $seqPlainText      .=     $thisPartSeqPT;
            $nucAccession       =     $accession;
            #print ("was " . length ($thisPartSeqPT) . " bp long\n");
        }
        else
        {
            #use current seqobj. not implemented
        }
    }
    #$| = 1;print (".");
    return($nucAccession,$seqPlainText);
}

sub getCodedBySeq($)
{
    my ($codedBy)         =    @_;
    my $commandString      =    $codedBy;
    my ($nucAccession,$seqPlainText) = '';
    my $strand            =    1;
    if($commandString =~ m/[\(\)]/)
    {
        while($commandString =~ m/[\(\)]/)
        {
            #get the command, and the stuff inside the brackets (called arguments here) may contain other strings
            my($command, $arguments) = split(/\(/,$commandString,2);
            $arguments =~ s/\)$//;
            if(grep(/join/,$command))
            {
                $commandString                  =     $arguments;
                ($nucAccession,$seqPlainText)   =    joinParts($arguments);
                last;
            }
            elsif(grep(/complement/,$command))
            {
                $commandString                  =     $arguments;
                $strand                         =    2;#tell us to use revcom
            }
        }
    }
    else
    {
        ($nucAccession,$seqPlainText)    =    joinParts($commandString);
    }
    
    if(!$nucAccession||!$seqPlainText){return(undef,undef);}
    
    #return text seq and accession
    if($strand ==1)
    {
        #$| = 1;print (".");
        return ($nucAccession,$seqPlainText);
    }
    else
    {
        my $seqObj    =    Bio::Seq->new(-seq => $seqPlainText);
        #$| = 1;print (".");
        return ($nucAccession,$seqObj->revcom->seq);
    }
}

sub designPrimerFromSeq ($$$) 
{
    my ($nucSeq,$truncationStart,$truncationEnd) = @_;
    
    if(!$nucSeq)
    {die("Bad call to designPrimerSeq $nucSeq,$truncationStart,$truncationEnd: Check your primer file");}
    
    my $pcrSeq                =    "";    #Returned
    $pcrSeq                   =    substr($nucSeq,$truncationStart,(length($nucSeq)-$truncationEnd));
    
    my $Fprimer               =    "";    #Returned
    my $FprimerATT            =    "";    #R
    my $FprimerTM             =    0;     #R
    my $FprimerTemplate       =    "";    #R
    my $Rprimer               =    "";    #R
    my $RprimerATT            =    "";    #R
    my $RprimerTM             =     0;     #R
    my $RprimerTemplate       =    '';    #R
    
    my $FPrimerTemplateObj    =     Bio::Seq->new(-seq=> $nucSeq);
    my $RPrimerTemplateObj    =     $FPrimerTemplateObj->revcom;
    
    my $maxPrimerLen          =    32;
    my $minTm                 =    59;
    my $FprimerLen            =    10;
    my $RprimerLen            =    10; #1 LESS THAN THE MINIMUM
    
    do #forwards
    {
        $Fprimer              =    substr($FPrimerTemplateObj->seq,$truncationStart,$FprimerLen);
        my $FprimerSeqobj     =    Bio::Seq->new(-seq=> $Fprimer);
        $FprimerTemplate      =    $FprimerSeqobj->seq;
        
        my $oligotmCommand    =     "$oligotm " . $Fprimer;
        my $pid               =     open3(\*WTRFH, \*RDRFH, \*ERRFH, $oligotmCommand);
        close (WTRFH);
        
        my ($tm, $errors);
        while (<RDRFH>) { $tm .= $_;}
        while (<ERRFH>) { $errors .= $_;}
        chomp $tm;
        
        $FprimerTM            =     $tm;
        $FprimerLen++;
    } while(($FprimerTM < $minTm)&& ($FprimerLen<$maxPrimerLen));
    #my $RprimerClamp    =    0;
    do #reverse
    {
        $Rprimer              =    substr($RPrimerTemplateObj->seq,$truncationEnd,$RprimerLen);
        my $RprimerSeqobj     =    Bio::Seq->new(-seq=> $Rprimer);
        $RprimerTemplate      =    $RprimerSeqobj->revcom->seq;
        
        my $oligotmCommand    =     "$oligotm " . $Rprimer;
        my $pid               =     open3(\*WTRFH, \*RDRFH, \*ERRFH, $oligotmCommand);
        close (WTRFH);
        
        my ($tm, $errors);
        while (<RDRFH>) { $tm .= $_;}
        while (<ERRFH>) { $errors .= $_;}
        chomp $tm;
        
        $RprimerTM            =    $tm;
        $RprimerLen++;
    } while(($RprimerTM <$minTm) && $RprimerLen<$maxPrimerLen);
    
    $FprimerATT               =    $fATT . $Fprimer;
    $RprimerATT               =    $rATT . $Rprimer;
    
    return ($Fprimer,$FprimerATT,$FprimerTM,$FprimerTemplate,$Rprimer,$RprimerATT,$RprimerTM,$RprimerTemplate,$pcrSeq);
}

open(OUTFILE,">$outfile");
#output fixed header in case names of output fields are mangled.
print OUTFILE (qq("Well Number","cDNASpecies","ShortName","Protein","Domains","ProtAccession","TruncStart","TruncEnd","NucAccession",
"Sequence","PCRSequence","5Primer","5PrimerATT","5PrimerTemplate","3Primer","3PrimerATT","3PrimerTemplate","5PrimerTM","3PrimerTM","PCRLength") . "\n");
close OUTFILE;

while(my $csvline = <$csvFH>) 
{
    open(OUTFILE,">>$outfile");

    if ($csvline->{'ProtAccession'})
    {

        my ($Fprimer,$FprimerATT,$FprimerTM,$FprimerTemplate,$Rprimer,$RprimerATT,$RprimerTM,$RprimerTemplate,$PCRPlainTextSeq);
        my ($nucAccession, $nucPlainTextSeq, $truncationStart, $truncationEnd);
        
        my $protAccession = $csvline->{'ProtAccession'};
        
        #get genpept entry for supplied accession
        my $protGenPeptObj = $genpeptCacheObj->get_Seq_by_acc($protAccession);
        
        if (!$protGenPeptObj)
        {warn("No sequence found for protein accession $protAccession, skipping it\n");next;}
        
        foreach my $cdsSeqFeatureObj (  grep { $_->primary_tag eq 'CDS' } $protGenPeptObj->get_SeqFeatures())
        {
            next unless( $cdsSeqFeatureObj->has_tag('coded_by') ); # skip CDSes with no coded_by
            #$| = 1;print (".");
            my ($codedby)                =    $cdsSeqFeatureObj->each_tag_value('coded_by');
            ($nucAccession,$nucPlainTextSeq)        =    getCodedBySeq($codedby);
        }
        
        if(!$nucAccession||!$nucPlainTextSeq){warn("\tNo nucelotide sequence found for protein accession $protAccession, skipping it\n");next;}
        
        
        if ($nucPlainTextSeq) 
        {
            #this is fairly confusing:    
            #truncation data is given from the start, as 1-indexed amino acids, so first we must multiply by three in either case.
            #for the start truncation, we have to subtract three so as not to skip the ATG codon. for a value of 1 this gives 1*3 = 3 -3 = 0 = ATGnnnnnn
            #for the end truncation, we have to supply the algorthim with the number of bases we want truncated from the end.
            #the algorthim uses a reverse compliment nucSeq to calculate the primer, so keep this in mind: pos(forwards) = length-pos(reverse)
            # so, for truncationEnd = 4, and a nucSeq of length 21, this gives:
            #4*3 = 12 bases from the start, so 21 -12 = 9 bases from the end. 
            #for the default (where we want to exclude the last codon)
            #say we want the truncation 2 -> 3 
            #ATGGTGATTTGA
            # 1  2  3  *
            #forwards:
            #2*3=6 -3 = 3 = ATG|->GTGATTTGA
            #rev:
            #3*3=12(len) - 9 = 3 = ATG|GTGATT<-|TGA
            $truncationStart        =    $csvline->{'TruncStart'} ? $csvline->{'TruncStart'} : 1; #in amino acid form
            $truncationStart        =    $truncationStart * 3 -3; #converted to dna form
            
            $truncationEnd          =    $csvline->{'TruncEnd'}   ? $csvline->{'TruncEnd'} :$protGenPeptObj->length; #we dont want the stop codon, if we did it would be $protGenPeptObj->length +1
            $truncationEnd          =    length($nucPlainTextSeq) - ($truncationEnd *3);
            
            ($Fprimer,$FprimerATT,$FprimerTM,$FprimerTemplate,$Rprimer,$RprimerATT,$RprimerTM,$RprimerTemplate,$PCRPlainTextSeq) = designPrimerFromSeq($nucPlainTextSeq,$truncationStart,$truncationEnd);
        }
        else
        {warn("No sequence found for nucelotide accession $nucAccession, skipping it\n");next;}
        
        $csvline->{'Sequence'}       = $nucPlainTextSeq;
        $csvline->{'PCRSequence'}    = $PCRPlainTextSeq;
        $csvline->{'NucAccession'}   = $nucAccession;
        $csvline->{'5Primer'}        = $Fprimer;
        $csvline->{'3Primer'}        = $Rprimer;
        $csvline->{'5PrimerATT'}     = $FprimerATT;
        $csvline->{'3PrimerATT'}     = $RprimerATT;
        $csvline->{'5PrimerTemplate'}= $FprimerTemplate;
        $csvline->{'3PrimerTemplate'}= $RprimerTemplate;
        $csvline->{'5PrimerTM'}      = $FprimerTM;
        $csvline->{'3PrimerTM'}      = $RprimerTM;
        $csvline->{'PCRLength'}      = length($PCRPlainTextSeq);
        
        print ($csvline->{'ShortName'} . "($protAccession)\nforward: " . $Fprimer . " len " .length($Fprimer) . " Tm = ".$FprimerTM . "\n");
        print ("Reverse: " . $Rprimer . " len " .length($Rprimer) . " Tm = ".$RprimerTM . "\n\n")    ;
        print OUTFILE ($csvline. "\n");
    }
    elsif ($csvline->{'NucAccession'})
    {
        my $nucAccession         =    $csvline->{'NucAccession'};
        my $nucGenBankObj        =    $genbankCacheObj->get_Seq_by_acc($nucAccession);
        
        if (!$nucGenBankObj) 
        {warn("No sequence found for nucelotide accession $nucAccession, skipping it\n");    next;}
        
        my $nucPlainTextSeq       =    $nucGenBankObj->seq;
        
        #if confused, see above
        my $truncationStart       =    $csvline->{'TruncStart'} ? $csvline->{'TruncStart'} : 1; #in amino acid form
        $truncationStart          =    $truncationStart * 3 -3; #converted to dna form
        
        my $truncationEnd         =    $csvline->{'TruncEnd'}   ? $csvline->{'TruncEnd'} : ($nucGenBankObj->length /3)-1; #we dont want the stop codon, if we did it would be $nucGenBankObj->length /3 as nuc seq includes the stop
        $truncationEnd            =    $nucGenBankObj->length - ($truncationEnd *3);
        
        my ($Fprimer,$FprimerATT,$FprimerTM,$FprimerTemplate,$Rprimer,$RprimerATT,$RprimerTM,$RprimerTemplate,$pcrSeq) = designPrimerFromSeq($nucPlainTextSeq,$truncationStart,$truncationEnd);
            
        $csvline->{'Sequence'}           = $nucPlainTextSeq;
        $csvline->{'PCRSequence'}        = $pcrSeq;        
        $csvline->{'5Primer'}            = $Fprimer;
        $csvline->{'3Primer'}            = $Rprimer;
        $csvline->{'5PrimerATT'}         = $FprimerATT;
        $csvline->{'3PrimerATT'}         = $RprimerATT;
        $csvline->{'5PrimerTemplate'}    = $FprimerTemplate;
        $csvline->{'3PrimerTemplate'}    = $RprimerTemplate;
        $csvline->{'5PrimerTM'}          = $FprimerTM;
        $csvline->{'3PrimerTM'}          = $RprimerTM;
        $csvline->{'PCRLength'}          = length($pcrSeq);
        
        print ($csvline->{'ShortName'} . "($nucAccession [from nuclotide accession])\n$nucPlainTextSeq\nforward: " . $Fprimer . " len " .length($Fprimer) . " Tm = ".$FprimerTM . "\n");
        print ("Reverse: " . $Rprimer . " len " .length($Rprimer) . " Tm = ".$RprimerTM . "\n\n")    ;
        print OUTFILE ($csvline. "\n");
        close OUTFILE;
    }
    elsif ($csvline->{'Sequence'})
    {
        my $nucPlainTextSeq        =    $csvline->{'Sequence'};
        
        #if confused, see above
        my $truncationStart        =    $csvline->{'TruncStart'} ? $csvline->{'TruncStart'} : 1; #in amino acid form
        $truncationStart           =    $truncationStart * 3 -3; #converted to dna form
        
        my $truncationEnd          =    $csvline->{'TruncEnd'}   ? $csvline->{'TruncEnd'} : (length($nucPlainTextSeq) /3) -1; #we dont want the stop codon, if we did it would be $nucGenBankObj->length /3 as nuc seq includes the stop
        $truncationEnd             =    length($nucPlainTextSeq) - ($truncationEnd *3);
         
        my ($Fprimer,$FprimerATT,$FprimerTM,$FprimerTemplate,$Rprimer,$RprimerATT,$RprimerTM,$RprimerTemplate,$pcrSeq) = designPrimerFromSeq($nucPlainTextSeq,$truncationStart,$truncationEnd);
        
        $csvline->{'PCRSequence'}        = $pcrSeq;
        $csvline->{'5Primer'}            = $Fprimer;
        $csvline->{'3Primer'}            = $Rprimer;
        $csvline->{'5PrimerATT'}         = $FprimerATT;
        $csvline->{'3PrimerATT'}         = $RprimerATT;
        $csvline->{'5PrimerTemplate'}    = $FprimerTemplate;
        $csvline->{'3PrimerTemplate'}    = $RprimerTemplate;
        $csvline->{'5PrimerTM'}          = $FprimerTM;
        $csvline->{'3PrimerTM'}          = $RprimerTM;
        $csvline->{'PCRLength'}          = length($pcrSeq);
        
        print ($csvline->{'ShortName'} . " (from raw seq)\nforward: " . $Fprimer . " len " .length($Fprimer) . " Tm = ".$FprimerTM . "\n");
        print ("Reverse: " . $Rprimer . " len " .length($Rprimer) . " Tm = ".$RprimerTM . "\n\n")    ;
        print OUTFILE ($csvline. "\n");
    }
    else
    {print OUTFILE ($csvline. "\n");}#print unchanged line
    
    close OUTFILE;
}
close $csvFH;
