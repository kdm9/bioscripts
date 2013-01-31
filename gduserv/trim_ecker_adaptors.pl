#!/usr/bin/perl 
while (<>){
    if ($_ =~ m/(.+)TCGTATG/g){
        print "$1\n";
    }
    elsif ($_ =~ m/(^>.+)/){
       print "$1\n";
    }
    else {print "\n";}
}


