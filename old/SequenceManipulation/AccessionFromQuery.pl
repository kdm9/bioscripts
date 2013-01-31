#!/usr/bin/perl
use Bio::DB::EUtilities;

my $searchterm	=	"(pap) AND Arabidopsis thaliana[Organism]";

my $factory = Bio::DB::EUtilities->new(-eutil  => 'esearch',
                                       -db     => 'protein',
                                       -term   => $searchterm,
                                       -email  => 'mymail@foo.bar',
                                       -retmax => 500000);
 
# query terms are mapped; what's the actual query?
print STDERR "Query translation: ",$factory->get_query_translation,"\n";
# query hits
print STDERR "Count = ",$factory->get_count,"\n";
# UIDs
my @ids = $factory->get_ids;
#print "length is: " .scalar(@ids) ."\n" . join(",",@ids). "\n";

my $counter = 0;
my @accs	=	();
while (scalar(@ids)>1)
{
	my $subset		=	scalar(@ids)>600? 600 :scalar(@ids)-1;
	my @idsSubset	=	@ids[0..$subset];
	
	my $factory = Bio::DB::EUtilities->new(-eutil   => 'efetch',
										   -db      => 'protein',
										   -id      => \@idsSubset,
										   -email   => 'mymail@foo.bar',
										   -rettype => 'acc');
	 
	@accs = (@accs,split(m{\n},$factory->get_Response->content));
	print join("\n",split(m{\n},$factory->get_Response->content))."\n";
#	print("before ".scalar(@ids) ."\t" .$ids[0] ."\t" .$ids[scalar(@ids)-1] .".\n");
	splice (@ids,0,$subset);
#	print("after ".scalar(@ids). "\t" .$ids[0] ."\t" .$ids[scalar(@ids)-1] .".\n");
 }
print join("\n",@accs), "\n";
