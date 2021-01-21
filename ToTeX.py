# This script creates a function which builds LaTeX formatted regression tables
# from a set of statsmodels.api.OLS fitted models and writes them to a txt file

# This currently does not (likely) handly small estiamted coefficients very well

def restab(list_of_regression_results, filepath):
    
    models = ['Model ' + str(i+1) + ' & ' for i in range(len(list_of_regression_results))]
    AR2 = [str(format(res.rsquared_adj, '.3f')) + ' & ' for res in list_of_regression_results]
    F = [str(format(res.fvalue[0][0], '.3f')) + ' & ' for res in list_of_regression_results]
    N = [str(int(res.nobs)) + ' & ' for res in list_of_regression_results]
    models.insert(0,'Variable & ')
    AR2.insert(0,'Adjusted $R^{2}$ & ')
    F.insert(0,'$F$-statistic & ')
    N.insert(0,'$N$ & ')
    exogs = []
    
    for res in list_of_regression_results:
        
        temp = res.params.to_dict()
        
        for key in temp:
            
            if key not in exogs:
                
                exogs.append(key)
    
    B = []
    BSE = []
    
    for x in exogs:
        
        B2 = []
        BSE2 = []
        
        for res in list_of_regression_results:
            
            betas = res.params.to_dict()
            stderr = res.bse.to_dict()
            
            if x in betas:
                
                stars = ''
                
                if list(res.pvalues)[list(betas.keys()).index(x)] < 0.01:
                    
                    stars = '***'
                    
                elif list(res.pvalues)[list(betas.keys()).index(x)] < 0.05:
                    
                    stars = '**'
                    
                elif list(res.pvalues)[list(betas.keys()).index(x)] < 0.1:
                    
                    stars = '*'
                    
                if abs(betas[x]) < 0.001:
                    
                    B2.append('{:.2e}'.format(betas[x]) + stars)
                    
                else:
                
                    B2.append(str(format(betas[x], '.3f')) + stars)
                    
                BSE2.append('(' + str(format(stderr[x], '.3f')) + ')')
            
            else:
                
                B2.append('---')
                BSE2.append('---')
        
        B.append(B2)
        BSE.append(BSE2)
    
    C = 'c' * len(models)
    begin_tabular = '\\begin{tabular}{'+ C + '}\hline\hline'
    header = ['\\begin{table}[h!]', '\centering', '\\footnotesize',
              '\caption{Estimates that are significant at the (10\%, 5\%, and 1\%) level are denoted by (*, **, and ***), respectively.}',
              '\label{restab}', begin_tabular, '\\rule{0pt}{3ex}']
    footer = ['\end{tabular}', '\end{table}']
    rule = '\\rule{0pt}{3ex}'
    
    models[len(models)-1] = models[len(models)-1][0:len(models[len(models)-1])-3] + '\\\\\hline'
    AR2[len(models)-1] = AR2[len(models)-1][0:len(AR2[len(models)-1])-3] + '\\\\'
    F[len(models)-1] = F[len(models)-1][0:len(F[len(models)-1])-3] + '\\\\\hline\hline'
    N[len(models)-1] = N[len(models)-1][0:len(N[len(models)-1])-3] + '\\\\'
    

    for b in range(len(B)):
        
        for i in range(len(B[b])-1):
            
            B[b][i] = str(B[b][i]) + ' & '
            BSE[b][i] = str(BSE[b][i]) + ' & '
        
        B[b].insert(0,str(exogs[b]) + ' & ')
        BSE[b].insert(0,' & ')    
        B[b][len(models)-1] = B[b][len(models)-1][0:len(B[b][len(models)-1])] + '\\\\'
        BSE[b][len(models)-1] = BSE[b][len(models)-1][0:len(BSE[b][len(models)-1])] + '\\\\'
    
    with open(filepath, 'w') as file:
        
        for h in header:
            
            file.write(h + '\n')
            
        file.write(''.join(models) + '\n')
        file.write(rule + '\n')
        
        for b in range(len(B)):
            
            file.write(''.join(B[b]) + '\n')
            file.write(rule + '\n')
            file.write(''.join(BSE[b]) + '\n')
            file.write(rule + '\n')
            
        file.write(''.join(N) + '\n')
        file.write(rule + '\n')
        file.write(''.join(AR2) + '\n')
        file.write(rule + '\n')
        file.write(''.join(F) + '\n')
        
        for f in footer:
            
            file.write(f + '\n')
        
        file.close()

def spatial_restab(list_of_regression_results, filepath):
    
    models = ['Model ' + str(i+1) + ' & ' for i in range(len(list_of_regression_results))]
    AR2 = [str(format(res.rsquared_adj, '.3f')) + ' & ' for res in list_of_regression_results]
    F = [str(format(res.fvalue, '.3f')) + ' & ' for res in list_of_regression_results]
    N = [str(int(res.nobs)) + ' & ' for res in list_of_regression_results]
    models.insert(0,'Variable & ')
    AR2.insert(0,'Adjusted $R^{2}$ & ')
    F.insert(0,'$F$-statistic & ')
    N.insert(0,'$N$ & ')
    exogs = []
    
    for res in list_of_regression_results:
        
        temp = res.params.to_dict()
        
        for key in temp:
            
            if key not in exogs:
                
                exogs.append(key)
    
    B = []
    BSE = []
    
    for x in exogs:
        
        B2 = []
        BSE2 = []
        
        for res in list_of_regression_results:
            
            betas = res.params.to_dict()
            stderr = res.bse.to_dict()
            
            if x in betas:
                
                stars = ''
                
                if res.pvalues[list(betas.keys()).index(x)] < 0.01:
                    
                    stars = '***'
                    
                elif res.pvalues[list(betas.keys()).index(x)] < 0.05:
                    
                    stars = '**'
                    
                elif res.pvalues[list(betas.keys()).index(x)] < 0.1:
                    
                    stars = '*'
                    
                if abs(betas[x]) < 0.001:
                    
                    B2.append('{:.2e}'.format(betas[x]) + stars)
                    
                else:
                
                    B2.append(str(format(betas[x], '.3f')) + stars)
                    
                BSE2.append('(' + str(format(stderr[x], '.3f')) + ')')
            
            else:
                
                B2.append('---')
                BSE2.append('---')
        
        B.append(B2)
        BSE.append(BSE2)
    
    C = 'c' * len(models)
    begin_tabular = '\\begin{tabular}{'+ C + '}\hline\hline'
    header = ['\\begin{table}[h!]', '\centering', '\\footnotesize',
              '\caption{Estimates that are significant at the (10\%, 5\%, and 1\%) level are denoted by (*, **, and ***), respectively.}',
              '\label{restab}', begin_tabular, '\\rule{0pt}{3ex}']
    footer = ['\end{tabular}', '\end{table}']
    rule = '\\rule{0pt}{3ex}'
    
    models[len(models)-1] = models[len(models)-1][0:len(models[len(models)-1])-3] + '\\\\\hline'
    AR2[len(models)-1] = AR2[len(models)-1][0:len(AR2[len(models)-1])-3] + '\\\\'
    F[len(models)-1] = F[len(models)-1][0:len(F[len(models)-1])-3] + '\\\\\hline\hline'
    N[len(models)-1] = N[len(models)-1][0:len(N[len(models)-1])-3] + '\\\\'
    

    for b in range(len(B)):
        
        for i in range(len(B[b])-1):
            
            B[b][i] = str(B[b][i]) + ' & '
            BSE[b][i] = str(BSE[b][i]) + ' & '
        
        B[b].insert(0,str(exogs[b]) + ' & ')
        BSE[b].insert(0,' & ')    
        B[b][len(models)-1] = B[b][len(models)-1][0:len(B[b][len(models)-1])] + '\\\\'
        BSE[b][len(models)-1] = BSE[b][len(models)-1][0:len(BSE[b][len(models)-1])] + '\\\\'
    
    with open(filepath, 'w') as file:
        
        for h in header:
            
            file.write(h + '\n')
            
        file.write(''.join(models) + '\n')
        file.write(rule + '\n')
        
        for b in range(len(B)):
            
            file.write(''.join(B[b]) + '\n')
            file.write(rule + '\n')
            file.write(''.join(BSE[b]) + '\n')
            file.write(rule + '\n')
            
        file.write(''.join(N) + '\n')
        file.write(rule + '\n')
        file.write(''.join(AR2) + '\n')
        file.write(rule + '\n')
        file.write(''.join(F) + '\n')
        
        for f in footer:
            
            file.write(f + '\n')
        
        file.close()

