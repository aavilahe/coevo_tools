function [ exit_status ] = hpDCAwrap( input_fasta, output_file, num_patterns )
%hpDCAwrap -- saves output of Weigt's inverse_hopfield_potts2()
%   runs inverse_hopfield_potts1() with default arguments
%   runs inverse_hopfield_potts2() with user-specified num_patterns
%   saves output of inverse_hopfield_potts2() to output_file

    [ Lambda, Vtilde, N, q ] = inverse_hopfield_potts1(input_fasta, 0.2, 0.5);
    F_apc = inverse_hopfield_potts2(Vtilde, Lambda, N, q, num_patterns );

    OUTFILE = fopen(output_file, 'w');
    %fprintf('would open file %s\n', output_file)
    for row_i = 1:size(F_apc,1)
        for col_j = (row_i+1):size(F_apc,2)
            fprintf(OUTFILE, '%d\t%d\t%f\n', row_i, col_j, F_apc(row_i, col_j));
            %fprintf('%d\t%d\t%f\n', row_i, col_j, F_apc(row_i, col_j))
        end
    end
    fclose(OUTFILE);
end

