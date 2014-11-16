#!/usr/bin/perl -w
opendir(DIR,".")||die "Cannot open .\n";
while(defined($file=readdir(DIR))) {
    if($file=~/^(.+)\.html$/o) {
	$ofile="$1\.spl";
	open(IN,$file)||die "Cannot open $file\n";
	open(OUT,">$ofile")||die "Cannot open $ofile\n";
	print "writing $ofile\n";
	while(defined($line=<IN>)) {
	    if($line=~/id=[0-9]+>([^<]+)<\/a>/o) {
		$text=$1;
		print OUT $text,"\n";
	    }
	}
	close(IN);
	close(OUT);
    }
}
closedir(DIR);
