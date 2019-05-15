//
// structured configuration; see #13752
//

#pragma once

// user macros
#define user_string(x) #x
#define user_render(x) user_string(x)
#define user_key_value(key) #key "=" user_render(key)

//#pragma message(user_key_value(USER_STAMP))

#ifdef USER_Wanhao_D6_MKS_SBASE
  #include "Wanhao_D6_MKS_SBASE/Configuration.h"
#endif

#ifdef USER_Custom_07_BIGTREE_SKR
  #include "Custom_07_BIGTREE_SKR/Configuration.h"
#endif
