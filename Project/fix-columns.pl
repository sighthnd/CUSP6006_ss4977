# Input: the CSV for Excel file from NYC Open Data of Dog Licenses
# Output: A semicolon delimited file with the same number of columns
# for each row
use strict;
open IN, "Dog_Licences.csv";
open OUT, "> Dog_Licences-munged.csv";
$_ = <IN>;
s/^[^A-Z]+//;
# Adding two columns to the dataset for the
# two possible values that the tract might be
# For example: A tract identified in this file as
# "501" could be either "000501" or "050100" and
# requires checking with the tract layer for later verification.
s/$/;boro_tract1;boro_tract2/;
print OUT;
while (<IN>) {
    s/\"//g;
    s/\r?\n$//;
    my @f;
    if (/\t/) {
	# If the record is tab delimited, change to semicolons
	# and remove the 5th element to keep the number of columns
	# consistent
	s/;+$//;
	s/^(\d+,\d+);/$1\t/;
	@f = split /\t/;
	splice @f, 4, 1;
    } else {
	# Remove any semicolons that might be in special characters that
	# are part of the name
	s/(\&\#\d\d);/$1~/;
	@f = split /;/;
    }
    # If the tract field has spaces, replace them with 0s, and the field
    # is ready
    $f[8] =~ tr/ /0/;
    # Remove rows that are not in the city
    if ($f[7] =~ /^\d+$/ and $f[8] =~ /^\d+$/ and $f[9] =~ /^[A-Z]{2}\d\d$/) {
	my $bor = substr $f[7], 0, 1;
	# The possibility that the tract is formed by adding "00" at
	# the end and then padding to the left
	if (length $f[8] <= 4) {
	    $f[15] = sprintf "%s%04d00", $bor, $f[8];
	} else {
	    $f[15] = sprintf "%s%6s", $bor, $f[8];
	    $f[15] =~ tr/ /0/;
	}
	# The possibity that it is just zero padded to the left
	$f[16] = sprintf "%s%6s", $bor, $f[8];
	$f[16] =~ tr/ /0/;
	chomp $f[14];
	chomp $f[15];
	# Put quotes around the number-like fields that are used as text
	foreach my $i (6..8, 15, 16) {
	    $f[$i] = qq/"$f[$i]"/;
	}
	$f[16] .= "\n";
	$f[0] =~ s/,//;
	$_ = join ';', @f;
	print OUT;
    }
}
