'''
Macbook 13 air specs by year 
Pulled from Wikipedia as of 2/13/14
Contains: Dictionary of year, technical specs, and corresponding regular expressions

Used: Determining whether or not it's an upgraded Macbook
'''

features_by_year = {
                    2008: { 
                            'processor_speeds': {
                                                    'low'  :r'1\.6',
                                                    'high' :r'1\.8'
                                                  },
                            #assume low for this feature
                            'memory': {
                                                 'low' :r'\b2 gb\b|\b2gb\b',
                                                'high' :None #r'\b2 gb\b|\b2gb\b',
                                    },
                            'HD':{
                                                 'low' :r'80',
                                                'high' :r'64'
                                }
                    },
                    2009: { 
                            'processor_speeds': {
                                        'low': r'1\.86|1\.8',
                                        'high': r'2\.13|2\.1'
                                              },
                            #assume low for this model
                            'memory': {
                                                 'low' :r'\b2 gb\b|\b2gb\b',
                                                'high' :None #r'\b2 gb\b|\b2gb\b',
                                    },
                            'HD':{
                                'low' :r'120',
                                'high':r'128'
                                }
                            },
                    2010: { 
                            'processor_speeds': {
                                        'low': r'1\.86|1\.8',
                                        'high': r'2\.13|2\.1'
                                              },
                            'memory': {
                                                 'low' :r'\b2 gb\b|\b2gb\b',
                                                'high' :r'\b4 gb\b|\b4gb\b',
                                    },
                            'HD':{
                                'low':r'128',
                                'high': r'256|250|516'
                                }
                        },
                    2011: { 
                            'processor_speeds': {
                                    'low': r'1\.7',
                                    'high': r'1\.8|1\.8'
                                              },
                            'memory': {
                                                 'low' :r'\b2 gb\b|\b2gb\b',
                                                'high' :r'\b4 gb\b|\b4gb\b',
                                    },
                            'HD':{
                                'low':r'128',
                                'high': r'256|250|516'
                                },
                            },
                    2012: { 
                            'processor_speeds': {
                                    'low': r'1\.8',
                                    'high': r'2\.0'
                                              },
                            'memory': {
                                                 'low' :r'\b4 gb\b|\b4gb\b',
                                                'high' :r'\b8 gb\b|\b8gb\b',
                                    },
                            'HD':{
                                'low':r'128',
                                'high': r'256|516'
                                },
                            },
                    2013: { 
                            'processor_speeds': {
                                    'low': r'1\.3',
                                    'high': r'1\.7'
                                              },
                            'memory': {
                                                 'low' :r'\b4 gb\b|\b4gb\b',
                                                'high' :r'\b8 gb\b|\b8gb\b',
                                    },
                            'HD':{
                                'low':r'128',
                                'high':r'256|250|516'
                                }
                    },
                    2014: { 
                            'processor_speeds': {
                                                    'low'  :r'1\.4',
                                                    'high' :r'1\.7'
                                                  },
                            
                            'memory': {
                                                 'low' :r'\b4 gb\b|\b4gb\b',
                                                'high' :r'\b8 gb\b|\b8gb\b',
                                    },
                            'HD':{
                                                  'low':r'128',
                                                 'high':r'256|250|516'
                                }
                          },
                  }

