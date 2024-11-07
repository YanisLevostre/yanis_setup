import maya.cmds as cmds


class Control(object):
    shapes = {
        'cube': {'shape': [(0.5, 0.5, -0.5),
                           (-0.5, 0.5, -0.5),
                           (-0.5, 0.5, 0.5),
                           (0.5, 0.5, 0.5),
                           (0.5, -0.5, 0.5),
                           (0.5, -0.5, -0.5),
                           (0.5, 0.5, -0.5),
                           (0.5, -0.5, -0.5),
                           (-0.5, -0.5, -0.5),
                           (-0.5, 0.5, -0.5),
                           (-0.5, -0.5, -0.5),
                           (-0.5, -0.5, 0.5),
                           (-0.5, 0.5, 0.5),
                           (-0.5, -0.5, 0.5),
                           (0.5, -0.5, 0.5),
                           (0.5, 0.5, 0.5),
                           (0.5, 0.5, -0.5)],
                 'degree': 1},
        'cylinder': {'shape': [[1.0, 0.3262669508210962, 0.0], [1.0, 0.3262669508210962, 0.0],
                               [0.9510571360588074, 0.3262669508210962, -0.3090171813964844],
                               [0.809017539024353, 0.3262669508210962, -0.5877856016159058],
                               [0.5877856016159058, 0.3262669508210962, -0.8090174794197083],
                               [0.309017151594162, 0.3262669508210962, -0.9510570168495178],
                               [0.0, 0.3262669508210962, -1.0000004768371582],
                               [0.0, 0.3262669508210962, -1.0000004768371582],
                               [-0.309017151594162, 0.3262669508210962, -0.951056957244873],
                               [-0.5877854824066162, 0.3262669508210962, -0.8090173006057739],
                               [-0.8090172410011292, 0.3262669508210962, -0.5877854228019714],
                               [-0.9510567784309387, 0.3262669508210962, -0.3090170621871948],
                               [-1.000000238418579, 0.3262669508210962, 0.0],
                               [-1.000000238418579, 0.3262669508210962, 0.0],
                               [-0.9510567784309387, 0.3262669508210962, 0.3090170621871948],
                               [-0.8090171813964844, 0.3262669508210962, 0.5877853631973267],
                               [-0.5877853631973267, 0.3262669508210962, 0.8090171217918396],
                               [-0.3090170621871948, 0.3262669508210962, 0.9510566592216492],
                               [-2.9802322387695312e-08, 0.3262669508210962, 1.0000001192092896],
                               [-2.9802322387695312e-08, 0.3262669508210962, 1.0000001192092896],
                               [0.30901697278022766, 0.3262669508210962, 0.9510565996170044],
                               [0.5877852439880371, 0.3262669508210962, 0.8090170621871948],
                               [0.80901700258255, 0.3262669508210962, 0.5877853035926819],
                               [0.9510565400123596, 0.3262669508210962, 0.30901700258255005],
                               [1.0, 0.3262669508210962, 0.0], [1.0, 0.3262669508210962, 0.0],
                               [1.0, -0.3262669508210962, 0.0], [1.0, -0.3262669508210962, 0.0],
                               [0.9510571360588074, -0.3262669508210962, -0.3090171813964844],
                               [0.809017539024353, -0.3262669508210962, -0.5877856016159058],
                               [0.5877856016159058, -0.3262669508210962, -0.8090174794197083],
                               [0.309017151594162, -0.3262669508210962, -0.9510570168495178],
                               [0.0, -0.3262669508210962, -1.0000004768371582],
                               [0.0, -0.3262669508210962, -1.0000004768371582],
                               [0.0, -0.3262669508210962, -1.0000004768371582],
                               [0.0, 0.3262669508210962, -1.0000004768371582],
                               [0.0, 0.3262669508210962, -1.0000004768371582],
                               [0.0, -0.3262669508210962, -1.0000004768371582],
                               [0.0, -0.3262669508210962, -1.0000004768371582],
                               [0.0, -0.3262669508210962, -1.0000004768371582],
                               [-0.309017151594162, -0.3262669508210962, -0.951056957244873],
                               [-0.5877854824066162, -0.3262669508210962, -0.8090173006057739],
                               [-0.8090172410011292, -0.3262669508210962, -0.5877854228019714],
                               [-0.9510567784309387, -0.3262669508210962, -0.3090170621871948],
                               [-1.000000238418579, -0.3262669508210962, 0.0],
                               [-1.000000238418579, -0.3262669508210962, 0.0],
                               [-1.000000238418579, 0.3262669508210962, 0.0],
                               [-1.000000238418579, 0.3262669508210962, 0.0],
                               [-1.000000238418579, -0.3262669508210962, 0.0],
                               [-1.000000238418579, -0.3262669508210962, 0.0],
                               [-0.9510567784309387, -0.3262669508210962, 0.3090170621871948],
                               [-0.8090171813964844, -0.3262669508210962, 0.5877853631973267],
                               [-0.5877853631973267, -0.3262669508210962, 0.8090171217918396],
                               [-0.3090170621871948, -0.3262669508210962, 0.9510566592216492],
                               [-2.9802322387695312e-08, -0.3262669508210962, 1.0000001192092896],
                               [-2.9802322387695312e-08, -0.3262669508210962, 1.0000001192092896],
                               [-2.9802322387695312e-08, 0.3262669508210962, 1.0000001192092896],
                               [-2.9802322387695312e-08, 0.3262669508210962, 1.0000001192092896],
                               [-2.9802322387695312e-08, -0.3262669508210962, 1.0000001192092896],
                               [-2.9802322387695312e-08, -0.3262669508210962, 1.0000001192092896],
                               [0.30901697278022766, -0.3262669508210962, 0.9510565996170044],
                               [0.5877852439880371, -0.3262669508210962, 0.8090170621871948],
                               [0.80901700258255, -0.3262669508210962, 0.5877853035926819],
                               [0.9510565400123596, -0.3262669508210962, 0.30901700258255005],
                               [1.0, -0.3262669508210962, 0.0], [1.0, -0.3262669508210962, 0.0]],
                     'degree': 1
                     },
        'double_arrow': dict(shape=[[0.938602579287048, 0.0, 0.0], [0.5631615647217083, 0.0, -0.5631615777930825],
                                    [0.5631615647217083, 0.0, -0.18772056322774391],
                                    [0.5631615647217083, 0.0, -0.18772056322774391],
                                    [-0.5631615908644596, 0.0, -0.18772056322774391],
                                    [-0.5631615908644596, 0.0, -0.5631615777930825],
                                    [-0.938602605429798, 0.0, 0.0],
                                    [-0.5631615908644596, 0.0, 0.5631615777930825],
                                    [-0.5631615908644596, 0.0, 0.18772050728266967],
                                    [0.5631615647217083, 0.0, 0.18772050728266967],
                                    [0.5631615647217083, 0.0, 0.5631615777930825], [0.938602579287048, 0.0, 0.0]],
                             degree=1),
        'locator': {'shape': [[0.5, 0.05000000074505806, -0.05000000074505806],
                              [-0.5, 0.05000000074505806, -0.05000000074505806],
                              [-0.5, 0.05000000074505806, 0.05000000074505806],
                              [0.5, 0.05000000074505806, 0.05000000074505806],
                              [0.5, 0.05000000074505806, -0.05000000074505806],
                              [0.5, -0.05000000074505806, -0.05000000074505806],
                              [-0.5, -0.05000000074505806, -0.05000000074505806],
                              [-0.5, 0.05000000074505806, -0.05000000074505806],
                              [-0.5, -0.05000000074505806, -0.05000000074505806],
                              [-0.5, -0.05000000074505806, 0.05000000074505806],
                              [-0.5, 0.05000000074505806, 0.05000000074505806],
                              [-0.5, -0.05000000074505806, 0.05000000074505806],
                              [0.5, -0.05000000074505806, 0.05000000074505806],
                              [0.5, 0.05000000074505806, 0.05000000074505806],
                              [0.5, -0.05000000074505806, 0.05000000074505806],
                              [0.5, -0.05000000074505806, -0.05000000074505806],
                              [0.5, -0.05000000074505806, 0.05000000074505806],
                              [0.05000000074505806, -0.05000000074505806, 0.05002099275588989],
                              [0.05000000074505806, -0.05000000074505806, 0.5],
                              [-0.05000000074505806, -0.05000000074505806, 0.5],
                              [-0.05000000074505806, -0.05000000074505806, -0.5],
                              [0.05000000074505806, -0.05000000074505806, -0.5],
                              [0.05000000074505806, -0.05000000074505806, 0.5],
                              [0.05000000074505806, 0.05000000074505806, 0.5],
                              [0.05000000074505806, -0.05000000074505806, 0.5],
                              [0.05000000074505806, 0.05000000074505806, 0.5],
                              [-0.05000000074505806, 0.05000000074505806, 0.5],
                              [-0.05000000074505806, -0.05000000074505806, 0.5],
                              [-0.05000000074505806, 0.05000000074505806, 0.5],
                              [-0.05000000074505806, 0.05000000074505806, -0.5],
                              [-0.05000000074505806, -0.05000000074505806, -0.5],
                              [-0.05000000074505806, 0.05000000074505806, -0.5],
                              [0.05000000074505806, 0.05000000074505806, -0.5],
                              [0.05000000074505806, -0.05000000074505806, -0.5],
                              [0.05000000074505806, 0.05000000074505806, -0.5],
                              [0.05000000074505806, 0.05000000074505806, 0.5],
                              [0.05000000074505806, -0.05000000074505806, 0.5],
                              [0.05000000074505806, 0.05000000074505806, 0.5],
                              [0.05000000074505806, -0.05000000074505806, 0.5],
                              [0.05000000074505806, -0.05000000074505806, 0.05002099275588989],
                              [0.05000000074505806, -0.5, 0.05000000074505806],
                              [-0.05000000074505806, -0.5, 0.05000000074505806],
                              [-0.05000000074505806, 0.5, 0.05000000074505806],
                              [0.05000000074505806, 0.5, 0.05000000074505806],
                              [0.05000000074505806, -0.5, 0.05000000074505806],
                              [0.05000000074505806, -0.5, -0.05000000074505806],
                              [-0.05000000074505806, -0.5, -0.05000000074505806],
                              [-0.05000000074505806, -0.5, 0.05000000074505806],
                              [-0.05000000074505806, -0.5, -0.05000000074505806],
                              [-0.05000000074505806, 0.5, -0.05000000074505806],
                              [-0.05000000074505806, 0.5, 0.05000000074505806],
                              [-0.05000000074505806, 0.5, -0.05000000074505806],
                              [0.05000000074505806, 0.5, -0.05000000074505806],
                              [0.05000000074505806, 0.5, 0.05000000074505806],
                              [0.05000000074505806, 0.5, -0.05000000074505806],
                              [0.05000000074505806, -0.5, -0.05000000074505806],
                              [0.05000000074505806, -0.5, 0.05000000074505806]],
                    'degree': 1}
        ,'sphere': dict(shape=[[1.0, 0.0, 0.0], [0.9659258127212524, 0.2588190734386444, 0.0],
                               [0.866025447845459, 0.4999999701976776, 0.0],
                               [0.7071067690849304, 0.7071067690849304, 0.0], [0.5, 0.8660253882408142, 0.0],
                               [0.258819043636322, 0.9659258127212524, 0.0], [0.0, 1.0, 0.0],
                               [-0.258819043636322, 0.9659258127212524, 0.0], [-0.5, 0.8660253882408142, 0.0],
                               [-0.7071067690849304, 0.7071067690849304, 0.0],
                               [-0.866025447845459, 0.4999999701976776, 0.0],
                               [-0.9659258127212524, 0.2588190734386444, 0.0], [-1.0, 0.0, 0.0],
                               [-0.9659258127212524, -0.2588190734386444, 0.0],
                               [-0.866025447845459, -0.4999999701976776, 0.0],
                               [-0.7071067690849304, -0.7071067690849304, 0.0], [-0.5, -0.8660253882408142, 0.0],
                               [-0.258819043636322, -0.9659258127212524, 0.0], [0.0, -1.0, 0.0],
                               [0.258819043636322, -0.9659258127212524, 0.0], [0.5, -0.8660253882408142, 0.0],
                               [0.7071067690849304, -0.7071067690849304, 0.0],
                               [0.866025447845459, -0.4999999701976776, 0.0],
                               [0.9659258127212524, -0.2588190734386444, 0.0], [1.0, 0.0, 0.0],
                               [0.8660253882408142, 0.0, 0.5], [0.5, 0.0, 0.8660253882408142], [0.0, 0.0, 1.0],
                               [-0.5, 0.0, 0.8660253882408142], [-0.8660253882408142, 0.0, 0.5], [-1.0, 0.0, 0.0],
                               [-0.8660253882408142, 0.0, -0.5], [-0.5, 0.0, -0.8660253882408142], [0.0, 0.0, -1.0],
                               [0.5, 0.0, -0.8660253882408142], [0.8660253882408142, 0.0, -0.5], [1.0, 0.0, 0.0],
                               [0.8660253882408142, 0.0, -0.5], [0.5, 0.0, -0.8660253882408142], [0.0, 0.0, -1.0],
                               [0.0, 0.2588190734386444, -0.9659258127212524],
                               [0.0, 0.4999999701976776, -0.866025447845459],
                               [0.0, 0.7071067690849304, -0.7071067690849304], [0.0, 0.8660253882408142, -0.5],
                               [0.0, 0.9659258127212524, -0.258819043636322], [0.0, 1.0, 0.0],
                               [0.0, 0.9659258127212524, 0.258819043636322], [0.0, 0.8660253882408142, 0.5],
                               [0.0, 0.7071067690849304, 0.7071067690849304],
                               [0.0, 0.4999999701976776, 0.866025447845459],
                               [0.0, 0.2588190734386444, 0.9659258127212524], [0.0, 0.0, 1.0],
                               [0.0, -0.2588190734386444, 0.9659258127212524],
                               [0.0, -0.4999999701976776, 0.866025447845459],
                               [0.0, -0.7071067690849304, 0.7071067690849304], [0.0, -0.8660253882408142, 0.5],
                               [0.0, -0.9659258127212524, 0.258819043636322], [0.0, -1.0, 0.0],
                               [0.0, -0.9659258127212524, -0.258819043636322], [0.0, -0.8660253882408142, -0.5],
                               [0.0, -0.7071067690849304, -0.7071067690849304],
                               [0.0, -0.4999999701976776, -0.866025447845459],
                               [0.0, -0.2588190734386444, -0.9659258127212524], [0.0, 0.0, -1.0]],
                        degree = 1),
        'square':{'shape':[[0.5, 0.0, -0.5], [-0.5, 0.0, -0.5], [-0.5, 0.0, 0.5], [0.5, 0.0, 0.5], [0.5, 0.0, -0.5]],
                  'degree':1},
        'square_lolipop': dict(shape=[[0.0, 0.003040791863255232, 0.0], [0.0, 0.4030407680213973, 0.0],
                                      [0.10000002384185791, 0.4030407680213973, 0.0],
                                      [0.10000002384185791, 0.6030407859027908, 0.0],
                                      [-0.09999999403953552, 0.6030407859027908, 0.0],
                                      [-0.09999999403953552, 0.4030407680213973, 0.0], [0.0, 0.4030407680213973, 0.0]],
                               degree = 1),
        'arrow': dict(
            shape=[[-0.061877394498136104, 0.0, -0.3066225670899849], [-0.061877394498136104, 0.0, 0.09337740906815717],
                   [-0.19999998807907104, 0.0, 0.09337740906815717], [0.0, 0.0, 0.2933774269495506],
                   [0.19999998807907104, 0.0, 0.09337740906815717], [0.06187742430045844, 0.0, 0.09337740906815717],
                   [0.06187742430045844, 0.0, -0.3066225670899849], [-0.061877394498136104, 0.0, -0.3066225670899849]],
            degree = 1),
        'chest': dict(shape=[[-1.3873198723892526e-10, 0.0005005003766709315, -0.9987230969862725],
                             [-0.309017151594162, 0.0, -0.951056957244873],
                             [-0.5877854824066162, 0.0, -0.8090173006057739],
                             [-0.8090172410011292, 0.0, -0.5877854228019714],
                             [-0.9510567784309387, 0.0, -0.3090170621871948], [-1.000000238418579, 0.0, 0.0],
                             [-0.9510567784309387, 0.0, 0.3090170621871948],
                             [-0.8090171813964844, 0.0, 0.5877853631973267],
                             [-0.5877853631973267, 0.0, 0.8090171217918396],
                             [-0.3090170621871948, 0.0, 0.9510566592216492],
                             [-2.9802322387695312e-08, 0.0, 1.0000001192092896],
                             [0.30901697278022766, 0.0, 0.9510565996170044],
                             [0.5877852439880371, 0.0, 0.8090170621871948], [0.80901700258255, 0.0, 0.5877853035926819],
                             [0.9510565400123596, 0.0, 0.30901700258255005], [1.0, 0.0, 0.0],
                             [0.9510571360588074, 0.0, -0.3090171813964844],
                             [0.809017539024353, 0.0, -0.5877856016159058],
                             [0.5877856016159058, 0.0, -0.8090174794197083],
                             [0.309017151594162, 0.0, -0.9510570168495178],
                             [-1.3873198723892526e-10, 0.0005005003766709315, -0.9987230969862725],
                             [-1.7329070186544937e-09, 0.14410981018791702, -0.9852171309393565],
                             [-3.3234347216205406e-09, 0.26990232116494106, -0.9599424781020408],
                             [-3.4941453023723438e-09, 0.39181812071311783, -0.9220636943847238],
                             [-8.499860213465999e-10, 0.512269959672154, -0.8810349236597684],
                             [3.6812765779648544e-09, 0.6337861963799252, -0.8232289135664536],
                             [8.682234450464046e-09, 0.7263806689269268, -0.7604011597014682],
                             [1.664963814734799e-08, 0.7807815842577519, -0.707621308604581],
                             [3.477558525172286e-08, 0.7909039565223756, -0.6696014738061657],
                             [0.20691828997743397, 0.7909039565223756, -0.6368288960496283],
                             [0.39358197505709674, 0.7909039565223756, -0.5417190057627771],
                             [0.5417191746674405, 0.7909039565223756, -0.39358187073034107],
                             [0.6368290649542918, 0.7909039565223756, -0.2069182179396321],
                             [0.6696012552433834, 0.7909039565223756, 6.955117045371894e-08],
                             [0.7076210965409198, 0.7807815568129791, 3.3299284566122534e-08],
                             [0.7604009175899927, 0.726380608407862, 1.7434327030590933e-08],
                             [0.8232285457826953, 0.6337861768013506, 8.575445046618321e-09],
                             [0.8810345687536809, 0.5122699388819307, 1.8029766951994347e-09],
                             [0.9220633150656621, 0.39181807913344247, -2.4553577692101086e-09],
                             [0.9599420456747729, 0.2699022759072009, -3.0449962859565893e-09],
                             [0.985216725309017, 0.1441097407907396, -1.8074833524501428e-09], [1.0, 0.0, 0.0],
                             [0.985216725309017, 0.1441097407907396, -1.8074833524501428e-09],
                             [0.9599420456747729, 0.2699022759072009, -3.0449962859565893e-09],
                             [0.9220633150656621, 0.39181807913344247, -2.4553577692101086e-09],
                             [0.8810345687536809, 0.5122699388819307, 1.8029766951994347e-09],
                             [0.8232285457826953, 0.6337861768013506, 8.575445046618321e-09],
                             [0.7604009175899927, 0.726380608407862, 1.7434327030590933e-08],
                             [0.7076210965409198, 0.7807815568129791, 3.3299284566122534e-08],
                             [0.6696012552433834, 0.7909039565223756, 6.955117045371894e-08],
                             [0.6368286774868461, 0.7909039565223756, 0.20691822788615774],
                             [0.5417187871999948, 0.7909039565223756, 0.3935818160989591],
                             [0.3935817490344201, 0.7909039565223756, 0.5417188865534875],
                             [0.20691817696609566, 0.7909039565223756, 0.6368287122624313],
                             [1.4819913810026897e-08, 0.7909039565223756, 0.6696013545968762],
                             [-4.4391086917450195e-09, 0.7807815499517856, 0.7076212218822815],
                             [-1.3979473174668003e-08, 0.726380608407862, 0.7604010034508989],
                             [-2.0852843082351803e-08, 0.6337861801716064, 0.823228631536194],
                             [-2.710686112039382e-08, 0.5122699430399748, 0.881034694506913],
                             [-3.0973771708559035e-08, 0.3918180947258211, 0.9220634175666527],
                             [-3.193193540224274e-08, 0.2699022759072009, 0.9599421662762448],
                             [-3.1094651334026026e-08, 0.14410976458405755, 0.9852168189269228],
                             [-2.9802322387695312e-08, 0.0, 1.0000001192092896],
                             [-3.1094651334026026e-08, 0.14410976458405755, 0.9852168189269228],
                             [-3.193193540224274e-08, 0.2699022759072009, 0.9599421662762448],
                             [-3.0973771708559035e-08, 0.3918180947258211, 0.9220634175666527],
                             [-2.710686112039382e-08, 0.5122699430399748, 0.881034694506913],
                             [-2.0852843082351803e-08, 0.6337861801716064, 0.823228631536194],
                             [-1.3979473174668003e-08, 0.726380608407862, 0.7604010034508989],
                             [-4.4391086917450195e-09, 0.7807815499517856, 0.7076212218822815],
                             [1.4819913810026897e-08, 0.7909039565223756, 0.6696013545968762],
                             [-0.20691817199283277, 0.7909039565223756, 0.6368287768403389],
                             [-0.39358177635011105, 0.7909039565223756, 0.5417189511313952],
                             [-0.5417188468046394, 0.7909039565223756, 0.3935818806768667],
                             [-0.6368287370914907, 0.7909039565223756, 0.20691827631958845],
                             [-0.6696013148480281, 0.7909039565223756, 6.955117045371894e-08],
                             [-0.7076212332617048, 0.780781563674172, 3.3299282493336125e-08],
                             [-0.7604010340206894, 0.7263806181116811, 1.7434324959641713e-08],
                             [-0.8232287102816926, 0.6337861963799252, 8.575441985292516e-09],
                             [-0.8810347458197858, 0.512269941311237, 1.802974187699589e-09],
                             [-0.9220635322790994, 0.3918181051207395, -2.4553602111564928e-09],
                             [-0.9599422830916138, 0.26990229355132533, -3.0449958241770513e-09],
                             [-0.9852169287690393, 0.1441097764807166, -1.8074856352636645e-09],
                             [-1.000000238418579, 0.0, 0.0],
                             [-0.9852169287690393, 0.1441097764807166, -1.8074856352636645e-09],
                             [-0.9599422830916138, 0.26990229355132533, -3.0449958241770513e-09],
                             [-0.9220635322790994, 0.3918181051207395, -2.4553602111564928e-09],
                             [-0.8810347458197858, 0.512269941311237, 1.802974187699589e-09],
                             [-0.8232287102816926, 0.6337861963799252, 8.575441985292516e-09],
                             [-0.7604010340206894, 0.7263806181116811, 1.7434324959641713e-08],
                             [-0.7076212332617048, 0.780781563674172, 3.3299282493336125e-08],
                             [-0.6696013148480281, 0.7909039565223756, 6.955117045371894e-08],
                             [-0.6368287370914907, 0.7909039565223756, -0.20691813721724758],
                             [-0.541718911382547, 0.7909039565223756, -0.39358177386347964],
                             [-0.3935818409280186, 0.7909039565223756, -0.5417188766069618],
                             [-0.20691822042626348, 0.7909039565223756, -0.6368288314717208],
                             [3.477558525172286e-08, 0.7909039565223756, -0.6696014738061657]],
                      degree = 1),
        'circle_lolipop': dict(shape=[[0.0, 0.002503318381440467, 0.0], [0.0, 0.3546466129859638, 0.0],
                                      [-0.037654414772987366, 0.36171969552053196, -8.620510730196906e-18],
                                      [-0.10299141705036163, 0.39958140034688694, -6.302150120698609e-18],
                                      [-0.1406424343585968, 0.4648186058224557, -2.3075233027029336e-18],
                                      [-0.1406424343585968, 0.5401706748129247, 2.306460375615803e-18],
                                      [-0.10299141705036163, 0.6054895349265454, 6.306086673233749e-18],
                                      [-0.037654414772987366, 0.6431471385480283, 8.611951065218207e-18],
                                      [0.037654414772987366, 0.6431471385480283, 8.611951065218207e-18],
                                      [0.10299141705036163, 0.6054895349265454, 6.306086673233749e-18],
                                      [0.1406424343585968, 0.5401706748129247, 2.306460375615803e-18],
                                      [0.1406424343585968, 0.4648186058224557, -2.3075233027029336e-18],
                                      [0.10299141705036163, 0.39958140034688694, -6.302150120698609e-18],
                                      [0.037654414772987366, 0.36171969552053196, -8.620510730196906e-18],
                                      [0.0, 0.3546466129859638, 0.0]],
                               degree = 1)



    }

    controls = []
    groups = []
    proxys = []
    lasts = []
    last = ''
    type = "simple_control"
    def __init__(self,
                 name='control',
                 shape='shape',
                 color=None):
        self.name = name
        self.shape = shape
        self.group = name + '_ctrl_offset'
        self.control = name + '_ctrl'
        self.proxy = name + '_proxyControl_loc'


    def simple_control(self,name = None):
        if name == None:
            name = self.name
        group = cmds.group(em=True, n=name + '_ctrl_offset')
        control = cmds.curve(p=self.shapes[self.shape]['shape'], d=self.shapes[self.shape]['degree'], n = name + '_ctrl')
        cmds.parent(control, group)
        self.last = control
        self.type = 'simple_control'
        return {'name':control,'group':group}

    def control_chain(self,nbr = 1):

        chain_names = []
        chain_groups = []

        for index in range(nbr):
            control = self.simple_control(name = "{}{}".format(self.name,index) )
            if index !=0:
                cmds.parent(control['group'],chain_names[-1])
            chain_names.append(control['name'])
            chain_groups.append(control['group'])

        self.controls = chain_names
        self.groups = chain_groups
        self.type = 'control_chain'

    def make_reversible(self,controlMatrix = None):
        def make_single_reversible(group = None,control = None):
            input_transform = cmds.connectionInfo(group+'.offsetParentMatrix', sfd = True)
            loc = cmds.spaceLocator(n = control.replace('_ctrl','_proxyControl_loc'))[0]
            cmds.parent(loc,control)
            cmds.setAttr(loc+'.translate',0,0,0)
            cmds.setAttr(loc + '.rotate', 0, 0, 0)
            cmds.setAttr(loc + '.scale', 1, 1, 1)
            multMx = cmds.createNode('multMatrix', n = input_transform.split('.')[0] + '_' + loc + '_multMatrix')
            cmds.connectAttr(controlMatrix + '.worldMatrix[0]',multMx+'.matrixIn[0]' )
            cmds.connectAttr(input_transform, multMx + '.matrixIn[1]')
            cmds.connectAttr(multMx+'.matrixSum',group+'.offsetParentMatrix', f = True)
            cmds.connectAttr(controlMatrix + '.worldMatrix[0]',loc + '.offsetParentMatrix')

        if self.type == "simple_control":
            make_single_reversible(self.group,self.control)
            self.last = self.proxy

        if self.type == "control_chain":
            make_single_reversible(self.groups[0],self.controls[0])
            self.proxys.append('{}{}_proxyControl_loc'.format(self.name,0))
            for index in range(len(self.groups)-1):
                index+=1
                input_transform = cmds.connectionInfo(self.groups[index] + '.offsetParentMatrix', sfd=True)
                loc = cmds.spaceLocator(n='{}{}_proxyControl_loc'.format(self.name,index))[0]
                cmds.parent(loc, self.controls[index])
                cmds.setAttr(loc + '.translate', 0, 0, 0)
                cmds.setAttr(loc + '.rotate', 0, 0, 0)
                cmds.setAttr(loc + '.scale', 1, 1, 1)
                multMx_1 = cmds.createNode('multMatrix', n=input_transform.split('.')[0] + '_' + loc + '_01_multMatrix')
                multMx_2 = cmds.createNode('multMatrix', n=input_transform.split('.')[0] + '_' + loc + '_02_multMatrix')
                cmds.connectAttr(input_transform, multMx_1 + '.matrixIn[0]')
                cmds.connectAttr(controlMatrix + '.worldMatrix[0]', multMx_1 + '.matrixIn[1]')
                cmds.connectAttr(controlMatrix + '.worldMatrix[0]', multMx_2 + '.matrixIn[0]')
                cmds.connectAttr(multMx_1 + '.matrixSum', multMx_2 + '.matrixIn[1]')
                cmds.connectAttr(multMx_2 + '.matrixSum', self.groups[index] + '.offsetParentMatrix', f=True)
                cmds.connectAttr(controlMatrix + '.worldMatrix[0]', loc + '.offsetParentMatrix')
                self.proxys.append(loc)
            self.lasts = self.proxys