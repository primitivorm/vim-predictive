if !g:predictive#disable_plugin
    set completefunc=predictive#complete
    "for acp plugin integracion
    if exists("g:loaded_acp") && g:loaded_acp
        let g:acp_behaviorUserDefinedFunction = 'predictive#complete'
        let g:acp_behaviorUserDefinedMeets = 'predictive#meetsForPredictive'
    endif
endif
