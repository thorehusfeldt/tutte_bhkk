while(<>) {
    chomp;
    s/^ *//;
    @a=split / +/;
    $last=-1;
    for($i=0;$i<=$#a;$i++) {
	if($a[$i] != 0) {
	    $last = $i;
	}
    }
    for($i=0;$i<=$last;$i++) {
	print $a[$i];
	if($i<$last) {
	    print " ";
	} else {
	    if($last >= 0) {
		print "\n";
	    }
	}
    }
}
