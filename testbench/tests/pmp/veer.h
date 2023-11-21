/* SPDX-License-Identifier: Apache-2.0
 * Copyright 2023 Antmicro, Ltd. <www.antmicro.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef __VEER_H
#define __VEER_H

#include <setjmp.h>

#define TRY do { jmp_buf try_buf; if(!setjmp(try_buf)){ fault_setjmp(try_buf);
#define CATCH } else {
#define END_TRY } } while(0)
#define THROW longjmp(try_buf, 1)

#endif
