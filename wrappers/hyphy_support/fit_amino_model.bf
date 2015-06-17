
function computeScalingFactorB(rateMatrix, baseFreqs) {
	B = 0;
	for (n1 = 0; n1 < Rows(rateMatrix); n1 = n1+1) {
		for (n2 = 0; n2 < Columns(rateMatrix); n2 = n2+1) {
			if (n2 != n1) {
				B = B + baseFreqs[n1]*baseFreqs[n2]*rateMatrix[n1][n2];
			}
		}
	}
	return B;
}

VERBOSITY_LEVEL = 1;

SetDialogPrompt ("Please specify a file containing a protein sequence alignment:");

DataSet 	  ds 		   = ReadDataFile (PROMPT_FOR_FILE);
DataSetFilter filteredData = CreateFilter (ds, 1);

fprintf (stdout,"\n______________READ THE FOLLOWING DATA______________\n", ds);


    // specifies model "_customAAModel"
    // select a matrix from TemplateModels/EmpiricalAA
//ExecuteAFile (HYPHY_LIB_DIRECTORY+"TemplateBatchFiles"+DIRECTORY_SEPARATOR+"TemplateModels"+DIRECTORY_SEPARATOR+"Custom_AA.mdl");
ExecuteAFile (HYPHY_LIB_DIRECTORY+"TemplateBatchFiles"+DIRECTORY_SEPARATOR+"TemplateModels"+DIRECTORY_SEPARATOR+"WAG_F.mdl");
//SelectTemplateModel(filteredData);

	// read in tree from file 
ACCEPT_BRANCH_LENGTHS 	= 1;
ACCEPT_ROOTED_TREES		= 1;
SetDialogPrompt ("Please select a file containing a tree with branch lengths: ");
fscanf(PROMPT_FOR_FILE, "String", tree_string);

Tree	aa_tree = tree_string;

//fprintf(stdout, Format(aa_tree, 0, 1), "\n");

    // constrain branch lengths 
global scalingB 		= computeScalingFactorB (_customAAModelMatrix, vectorOfFrequencies);

branchNames 	= BranchName (aa_tree, -1);
branchLengths	= BranchLength (aa_tree, -1);

for (k = 0; k < Columns(branchNames)-1; k=k+1)
{
	ExecuteCommands("aa_tree." + branchNames[k] + ".t:=" + branchLengths[k] + "/scalingB;");
}



SetDialogPrompt("Select a file to save likelihood function");
LikelihoodFunction lf = (filteredData, aa_tree);

AUTO_PARALLELIZE_OPTIMIZE = 1;
timer                 = Time(0);
Optimize                (res,lf);
timer                 = Time(0)-timer;

fprintf (stdout, "\n______________RESULTS______________\nTime taken = ", timer, " seconds\nAIC Score = ", 
				  2(res[1][1]-res[1][0]),"\n",lf);


LIKELIHOOD_FUNCTION_OUTPUT = 7;
fprintf(PROMPT_FOR_FILE, lf);
