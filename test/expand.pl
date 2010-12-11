while(<>) {
    chomp;
    @s=split //;
    $n2=$#s+1;
    $n=int(sqrt($n2));
    print "$n ",join(' ',@s),"\n";
}
