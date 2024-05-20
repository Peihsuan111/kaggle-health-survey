import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
# Updated HTML content with a shorter table as provided by the user
html_content = """
<table class="table table-bordered table-striped" cellspacing="0" rules="all" border="1" id="GridView1" style="border-collapse:collapse;">
		<thead>
			<tr style="background-color:#CDCDCD;">
				<th scope="col">Variable Name</th><th scope="col">Variable Description</th><th scope="col">Data File Name</th><th scope="col">Data File Description</th><th scope="col">Begin Year</th><th scope="col">EndYear</th><th scope="col">Component</th><th scope="col">Use Constraints</th>
			</tr>
		</thead><tbody>
			<tr>
				<td>DLQ010</td><td>With this next set of questions, we want to learn about people who have physical, mental, or emotional conditions that cause serious difficulties with their daily activities. Though different, these questions may sound similar to ones I asked earlier. {Are you/Is SP} deaf or {do you/does he/does she} have serious difficulty hearing?</td><td>DLQ_H</td><td>Disability</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DLQ020</td><td>{Are you/Is SP} blind or {do you/does he/does she} have serious difficulty seeing even when wearing glasses?</td><td>DLQ_H</td><td>Disability</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DLQ040</td><td>Because of a physical, mental, or emotional condition, {do you/does he/does she} have serious difficulty concentrating, remembering, or making decisions?</td><td>DLQ_H</td><td>Disability</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DLQ050</td><td>{Do you/Does SP} have serious difficulty walking or climbing stairs?</td><td>DLQ_H</td><td>Disability</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DLQ060</td><td>{Do you/Does SP} have difficulty dressing or bathing?</td><td>DLQ_H</td><td>Disability</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DLQ080</td><td>Because of a physical, mental, or emotional condition, {do you/does he/does she} have difficulty doing errands alone such as visiting a doctor's office or shopping?</td><td>DLQ_H</td><td>Disability</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>DLQ_H</td><td>Disability</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DED031</td><td>If after several months of not being in the sun, {you/SP} then went out in the sun without sunscreen or protective clothing for a half hour, which one of these would happen to {your/his/her} skin?</td><td>DEQ_H</td><td>Dermatology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DED120</td><td>The next questions ask about the time you spent outdoors during the past 30 days. By outdoors, I mean outside and not under any shade. How much time did you usually spend outdoors between 9 in the morning and 5 in the afternoon 
on the days that you worked or went to school?</td><td>DEQ_H</td><td>Dermatology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DED125</td><td>During the past 30 days, how much time did you usually spend outdoors between 9 in the morning and 5 in the afternoon on the days when you were not working or going to school?</td><td>DEQ_H</td><td>Dermatology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DEQ034A</td><td>When {you go/SP goes} outside on a very sunny day, for more than one hour, how often {do you/does SP} Stay in the shade?</td><td>DEQ_H</td><td>Dermatology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DEQ034C</td><td>Wear a long sleeved shirt?  Would you say . . .</td><td>DEQ_H</td><td>Dermatology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DEQ034D</td><td>Use sunscreen?  Would you say . . .</td><td>DEQ_H</td><td>Dermatology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DEQ038G</td><td>How many times in the past year {have you/has SP} had a sunburn?</td><td>DEQ_H</td><td>Dermatology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DEQ038Q</td><td>How many times in the past year {have you/has SP} had a sunburn?</td><td>DEQ_H</td><td>Dermatology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>DEQ_H</td><td>Dermatology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030aa</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} hip the 1st time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030ab</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} hip the 2nd time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030ac</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} hip the 3rd time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030ba</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} wrist the 1st time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030bb</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} wrist 2nd time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030bc</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} wrist the 3rd time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030bd</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} wrist the 4th time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030be</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} wrist the 5th time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030bf</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} wrist the 6th time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030bg</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} wrist the 7th time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030bh</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} {hip/wrist/spine} {the {1st/2nd/10th or more recent time . . .} time}?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030bi</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} {hip/wrist/spine} {the {1st/2nd/10th or more recent time . . .} time}?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030bj</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} {hip/wrist/spine} {the {1st/2nd/10th or more recent time . . .} time}?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030ca</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} spine the 1st time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030cb</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} spine the 2nd time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD030cc</td><td>How old {were you/was SP} when {you/s/he} fractured {your/his/her} spine the 3rd time?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD050aa</td><td>Did that fracture occur as a result of . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD050ab</td><td>Did that fracture occur as a result of . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD050ac</td><td>Did that fracture occur as a result of . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD050ba</td><td>Did that fracture occur as a result of. . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD050bb</td><td>Did that fracture occur as a result of . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD050bc</td><td>Did that fracture occur as a result of . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD050bd</td><td>Did that fracture occur as a result of.....</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD050ca</td><td>Did that fracture occur as a result of . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD050cb</td><td>Did that fracture occur as a result of . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD110a</td><td>How old {were you/was SP} when {you/SP} fractured {your/his/her} (fracture site selected in OSQ100a) for the first time after age 20?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD110b</td><td>How old {were you/was SP} when {you/SP} fractured {your/his/her} (fracture site selected in OSQ100b) for the first time after age 20?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD110c</td><td>How old {were you/was SP} when {you/SP} fractured {your/his/her} (fracture site selected in OSQ100c) for the first time after age 20?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD110d</td><td>How old {were you/was SP} when {you/SP} fractured {your/his/her} (fracture site selected in OSQ100d) for the first time after age 20?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD110e</td><td>How old {were you/was SP} when {you/SP} fractured {your/his/her} (fracture site selected in OSQ100e) for the first time after age 20?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSD110g</td><td>How old {were you/was SP} when {you/SP} fractured {your/his/her} (fracture site selected in OSQ100d) for the first time after age 20?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ010a</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured {your/his/her} . . .hip?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ010b</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured {your/his/her} . . .wrist?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ010c</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured {your/his/her} . . .spine?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ020a</td><td>How many times {have you/has SP} broken or fractured {your/his/her} hip?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ020b</td><td>How many times {have you/has SP} broken or fractured {your/his/her} wrist?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ020c</td><td>How many times {have you/has SP} broken or fractured {your/his/her} spine?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040aa</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040ab</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040ac</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040ba</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040bb</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040bc</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040bd</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040be</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040bf</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040bg</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040bh</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040bi</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040bj</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040ca</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040cb</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ040cc</td><td>{Were you/Was SP} . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ060</td><td>Has a doctor ever told {you/SP} that {you/s/he} had osteoporosis, sometimes called thin or brittle bones?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ072</td><td>Please look at the drugs on this card that are prescribed for osteoporosis. {Have you/Has SP} ever been told by a doctor or other health care professional to take a prescribed medicine for osteoporosis?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ080</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured any other bone after {you were/s/he was} 20 years of age?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ090a</td><td>Was this fracture the result of severe trauma such as a car accident, being struck by a vehicle, a physical attack, or a hard fall such as falling off a ladder or down stairs?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ090b</td><td>Was this fracture the result of severe trauma such as a car accident, being struck by a vehicle, a physical attack, or a hard fall such as falling off a ladder or down stairs?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ090c</td><td>Was this fracture the result of severe trauma such as a car accident, being struck by a vehicle, a physical attack, or a hard fall such as falling off a ladder or down stairs?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ090d</td><td>Was this fracture the result of severe trauma such as a car accident, being struck by a vehicle, a physical attack, or a hard fall such as falling off a ladder or down stairs?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ090e</td><td>Was this fracture the result of severe trauma such as a car accident, being struck by a vehicle, a physical attack, or a hard fall such as falling off a ladder or down stairs?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ090f</td><td>Was this fracture the result of severe trauma such as a car accident, being struck by a vehicle, a physical attack, or a hard fall such as falling off a ladder or down stairs?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ090g</td><td>Was this fracture the result of severe trauma such as a car accident, being struck by a vehicle, a physical attack, or a hard fall such as falling off a ladder or down stairs?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ090h</td><td>Was this fracture the result of severe trauma such as a car accident, being struck by a vehicle, a physical attack, or a hard fall such as falling off a ladder or down stairs?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ100a</td><td>Please look at this card and tell me where the fracture occurred.</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ100b</td><td>Please look at this card and tell me where the fracture occurred.</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ100c</td><td>Please look at this card and tell me where the fracture occurred.</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ100d</td><td>Please look at this card and tell me where the fracture occurred.</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ100e</td><td>Please look at this card and tell me where the fracture occurred.</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ100g</td><td>Please look at this card and tell me where the fracture occurred.</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ120a</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured any other bones after {you were/s/he was} 20 years of age?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ120b</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured any other bones after {you were/s/he was} 20 years of age?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ120c</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured any other bones after {you were/s/he was} 20 years of age?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ120d</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured any other bones after {you were/s/he was} 20 years of age?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ120e</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured any other bones after {you were/s/he was} 20 years of age?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ120f</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured any other bones after {you were/s/he was} 20 years of age?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ120g</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured any other bones after {you were/s/he was} 20 years of age?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ120h</td><td>Has a doctor ever told {you/SP} that {you/s/he} had broken or fractured any other bones after {you were/s/he was} 20 years of age?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ130</td><td>{Have you/has SP} ever taken any prednisone or cortisone pills nearly every day for a month or longer?  [Prednisone and cortisone are types of steroids.]</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ140q</td><td>Please think about {your/SP's} use of prednisone or cortisone during {your/his/her} lifetime.  For how long did {you/s/he} use prednisone or cortisone nearly every day?  Do not count the months or years when {you were/s/he was} not taking the medicine.</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ140u</td><td>How long used prednisone or cortisone: month, year?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ150</td><td>Including living and deceased, were either of {your/SP's} biological parents ever told by a health professional that they had osteoporosis or brittle bones?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ160a</td><td>Mother was told had osteoporosis?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ160b</td><td>Father was told had osteoporosis?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ170</td><td>Did {your/SP's} biological mother ever fracture her hip?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ180</td><td>About how old was your mother when she fractured her hip (the first time)?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ190</td><td>Was she. . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ200</td><td>Did {your/SP's} biological father ever fracture his hip?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ210</td><td>About how old was your father when he fractured his hip (the first time)?</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OSQ220</td><td>Was he . . .</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>OSQ_H</td><td>Osteoporosis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>IMQ011</td><td>Hepatitis (Hep-a-ti-tis) A vaccine is given as a two dose series to some children older than 2 years and also to some adults, especially people who travel outside the United States.  It has only been available since 1995.  {Have you/Has SP} ever received hepatitis A vaccine?</td><td>IMQ_H</td><td>Immunization</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>IMQ020</td><td>Hepatitis (Hep-a-ti-tis) B vaccine is given in three separate doses and has been recommended for all newborn infants since 1991.  In 1995, it was recommended that adolescents be given the vaccine.  Persons who may be exposed to other people's blood, such as health care workers, also may have received the vaccine.  {Have you/Has SP} ever received the 3-dose series of the hepatitis B vaccine?</td><td>IMQ_H</td><td>Immunization</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>IMQ040</td><td>Human Papillomavirus (HPV) vaccine is given to prevent cervical cancer in girls and women.  There are two HPV vaccines available called Cervarix and Gardasil.  It is given in 3 separate doses over a 6 month period.  {Have you/Has SP} ever received one or more doses of the HPV vaccine?</td><td>IMQ_H</td><td>Immunization</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>IMQ045</td><td>How many doses of {Cervarix/Gardasil/the vaccine} {have you/has SP} received?</td><td>IMQ_H</td><td>Immunization</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>IMQ070</td><td>Human Papillomavirus (HPV) vaccine is given to prevent HPV infection and genital warts in boys and men.  It is given in 3 separate doses over a 6 month period.  {Have you/Has SP} ever received one or more doses of the HPV vaccine? (The brand name for the vaccine is Gardasil.)</td><td>IMQ_H</td><td>Immunization</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>IMQ080</td><td>Which of the HPV vaccines did {you/SP} receive, Cervarix or Gardasil?</td><td>IMQ_H</td><td>Immunization</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>IMQ090</td><td>How old {were you/was SP} when {you/SP} received your first dose of {Cervarix/Gardasil/the vaccine}?</td><td>IMQ_H</td><td>Immunization</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>IMQ_H</td><td>Immunization</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD021</td><td>Ever had vaginal, anal, or oral sex.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD031</td><td>How old were you when you had sex for the first time?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD101</td><td>In your lifetime, with how many men have you had any kind of sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD171</td><td>In your lifetime, with how many women have you had any kind of sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD450</td><td>In the past 12 months, with how many men have you had any kind of sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD510</td><td>In the past 12 months, with how many women have you had any kind of sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD621</td><td>How old were you when you first performed oral sex on a man? Performing oral sex means your mouth on a man's penis or genitals.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD630</td><td>How long has it been since the last time you performed oral sex on a new male partner? A new sexual partner is someone that you had never had sex with before.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD633</td><td>How old were you when you first performed oral sex on a woman? Performing oral sex means your mouth on a woman's vagina or genitals.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXD642</td><td>How long has it been since the last time you performed oral sex on a new female partner? A new sexual partner is someone that you had never had sex with before.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ130</td><td>In your lifetime with how many women have you had sex? By sex, we mean sexual contact with another woman's vagina or genitals.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ251</td><td>In the past 12 months, about how often have you had {vaginal or anal/vaginal/anal} sex without using a condom?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ260</td><td>Has a doctor or other health care professional ever told you that you had genital herpes?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ265</td><td>Has a doctor or other health care professional ever told you that you had genital warts?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ267</td><td>How old were you when you were first told that you had genital warts?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ270</td><td>In the past 12 months, has a doctor or other health care professional told you that you had gonorrhea, sometimes called GC or clap?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ272</td><td>In the past 12 months, has a doctor or other health care professional told you that you had chlamydia?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ280</td><td>Are you circumcised or uncircumcised?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ292</td><td>Do you think of yourself as...</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ294</td><td>Do you think of yourself as...</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ410</td><td>In your lifetime, with how many men have you had anal or oral sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ490</td><td>In the past 12 months, with how many women have you had sex? By sex, we mean sexual contact with another woman's vagina or genitals.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ550</td><td>In the past 12 months, with how many men have you had anal or oral sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ590</td><td>Of the persons you had any kind of sex with in the past 12 months, how many were five or more years older than you?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ600</td><td>Of the persons you had any kind of sex with in the past 12 months, how many were five or more years younger than you?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ610</td><td>In the past 12 months, about how many times have you had {vaginal or anal/vaginal/anal} sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ624</td><td>In your lifetime, on how many men have you performed oral sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ627</td><td>In the past 12 months, on how many men have you performed oral sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ636</td><td>In your lifetime, on how many women have you performed oral sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ639</td><td>In the past 12 months, on how many women have you performed oral sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ645</td><td>When you performed oral sex in the past 12 months, how often would you use protection, like a condom or dental dam?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ648</td><td>In the past 12 months, did you have any kind of sex with a person that you never had sex with before?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ700</td><td>Have you ever had vaginal sex, also called sexual intercourse, with a man? This means a man's penis in your vagina.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ703</td><td>Have you ever performed oral sex on a man? This means putting your mouth on a man's penis or genitals.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ706</td><td>Have you ever had anal sex? This means contact between a man's penis and your anus or butt.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ709</td><td>Have you ever had any kind of sex with a woman? By sex, we mean sexual contact with another woman's vagina or genitals.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ724</td><td>In your lifetime, with how many men have you had vaginal sex?  Vaginal sex means a man's penis in your vagina.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ727</td><td>In the past 12 months, with how many men have you had vaginal sex? Vaginal sex means a man's penis in your vagina.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ741</td><td>Have you ever performed oral sex on a woman? Performing oral sex means your mouth on a woman's vagina or genitals.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ753</td><td>Has a doctor or other health care professional ever told you that you had human papillomavirus or HPV?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ800</td><td>Have you ever had vaginal sex, also called sexual intercourse, with a woman? This means your penis in a woman's vagina.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ803</td><td>Have you ever performed oral sex on a woman? This means putting your mouth on a woman's vagina or genitals.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ806</td><td>Have you ever had anal sex with a woman? Anal sex means contact between your penis and a woman's anus or butt.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ809</td><td>Have you ever had any kind of sex with a man, including oral or anal?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ824</td><td>In your lifetime, with how many women have you had vaginal sex? Vaginal sex means your penis in a woman's vagina.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ827</td><td>In the past 12 months, with how many women have you had vaginal sex? Vaginal sex means your penis in a woman's vagina.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ836</td><td>In your lifetime, with how many men have you had anal sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ841</td><td>In the past 12 months, with how many men have you had anal sex?</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SXQ853</td><td>Have you ever performed oral sex on a man? Performing oral sex means your mouth on a man's penis or genitals.</td><td>SXQ_H</td><td>Sexual Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD021</td><td>Ever had vaginal, anal, or oral sex.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD031</td><td>How old were you when you had sex for the first time?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD101</td><td>In your lifetime, with how many men have you had any kind of sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD171</td><td>In your lifetime, with how many women have you had any kind of sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD450</td><td>In the past 12 months, with how many men have you had any kind of sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD510</td><td>In the past 12 months, with how many women have you had any kind of sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD621</td><td>How old were you when you first performed oral sex on a man? Performing oral sex means your mouth on a man's penis or genitals.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD630</td><td>How long has it been since the last time you performed oral sex on a new male partner? A new sexual partner is someone that you had never had sex with before.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD633</td><td>How old were you when you first performed oral sex on a woman? Performing oral sex means your mouth on a woman's vagina or genitals.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXD642</td><td>How long has it been since the last time you performed oral sex on a new female partner? A new sexual partner is someone that you had never had sex with before.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ130</td><td>In your lifetime with how many women have you had sex? By sex, we mean sexual contact with another woman's vagina or genitals.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ251</td><td>In the past 12 months, about how often have you had {vaginal or anal/vaginal/anal} sex without using a condom?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ260</td><td>Has a doctor or other health care professional ever told you that you had genital herpes?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ265</td><td>Has a doctor or other health care professional ever told you that you had genital warts?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ267</td><td>How old were you when you were first told that you had genital warts?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ270</td><td>In the past 12 months, has a doctor or other health care professional told you that you had gonorrhea, sometimes called GC or clap?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ272</td><td>In the past 12 months, has a doctor or other health care professional told you that you had chlamydia?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ280</td><td>Are you circumcised or uncircumcised?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ410</td><td>In your lifetime, with how many men have you had anal or oral sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ490</td><td>In the past 12 months, with how many women have you had sex? By sex, we mean sexual contact with another woman's vagina or genitals.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ550</td><td>In the past 12 months, with how many men have you had anal or oral sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ590</td><td>Of the persons you had any kind of sex with in the past 12 months, how many were five or more years older than you?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ600</td><td>Of the persons you had any kind of sex with in the past 12 months, how many were five or more years younger than you?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ610</td><td>In the past 12 months, about how many times have you had {vaginal or anal/vaginal/anal} sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ624</td><td>In your lifetime, on how many men have you performed oral sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ627</td><td>In the past 12 months, on how many men have you performed oral sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ636</td><td>In your lifetime, on how many women have you performed oral sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ639</td><td>In the past 12 months, on how many women have you performed oral sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ645</td><td>When you performed oral sex in the past 12 months, how often would you use protection, like a condom or dental dam?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ648</td><td>In the past 12 months, did you have any kind of sex with a person that you never had sex with before?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ700</td><td>Have you ever had vaginal sex, also called sexual intercourse, with a man? This means a man's penis in your vagina.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ703</td><td>Have you ever performed oral sex on a man? This means putting your mouth on a man's penis or genitals.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ706</td><td>Have you ever had anal sex? This means contact between a man's penis and your anus or butt.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ709</td><td>Have you ever had any kind of sex with a woman? By sex, we mean sexual contact with another woman's vagina or genitals.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ724</td><td>In your lifetime, with how many men have you had vaginal sex?  Vaginal sex means a man's penis in your vagina.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ727</td><td>In the past 12 months, with how many men have you had vaginal sex? Vaginal sex means a man's penis in your vagina.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ741</td><td>Have you ever performed oral sex on a woman? Performing oral sex means your mouth on a woman's vagina or genitals.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ753</td><td>Has a doctor or other health care professional ever told you that you had human papillomavirus or HPV?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ800</td><td>Have you ever had vaginal sex, also called sexual intercourse, with a woman? This means your penis in a woman's vagina.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ803</td><td>Have you ever performed oral sex on a woman? This means putting your mouth on a woman's vagina or genitals.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ806</td><td>Have you ever had anal sex with a woman? Anal sex means contact between your penis and a woman's anus or butt.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ809</td><td>Have you ever had any kind of sex with a man, including oral or anal?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ824</td><td>In your lifetime, with how many women have you had vaginal sex? Vaginal sex means your penis in a woman's vagina.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ827</td><td>In the past 12 months, with how many women have you had vaginal sex? Vaginal sex means your penis in a woman's vagina.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ836</td><td>In your lifetime, with how many men have you had anal sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ841</td><td>In the past 12 months, with how many men have you had anal sex?</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SXQ853</td><td>Have you ever performed oral sex on a man? Performing oral sex means your mouth on a man's penis or genitals.</td><td>SXQY_H_R</td><td>Sexual Behavior - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>CDQ001</td><td>{Have you/Has SP} ever had any pain or discomfort in {your/her/his} chest?</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ002</td><td>{Do you/Does she/Does he} get it when {you/she/he} walk uphill or hurry?</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ003</td><td>{Do you/Does she/Does he} get it when {you/she/he} walk at an ordinary pace on level ground?</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ004</td><td>What {do you/does she/does he} do if {you/she/he} get it while {you/she/he} are walking?  {Do you/Does she/Does he} stop or slow down or continue at the same pace?</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ005</td><td>If {you/she/he} stand still, what happens to it?  Is the pain or discomfort relieved or not relieved?</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ006</td><td>How soon is the pain relieved?  Would you say...</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ008</td><td>Have {you/she/he} ever had a severe pain across the front of {your/her/his} chest lasting for half an hour or more?</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ009A</td><td>Please look at this card and show me where the pain or discomfort is located.</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ009B</td><td>Please look at this card and show me where the pain or discomfort is located.</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ009C</td><td>Please look at this card and show me where the pain or discomfort is located.</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ009D</td><td>Please look at this card and show me where the pain or discomfort is located.</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ009E</td><td>Please look at this card and show me where the pain or discomfort is located.</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ009F</td><td>Please look at this card and show me where the pain or discomfort is located.</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ009G</td><td>Please look at this card and show me where the pain or discomfort is located.</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ009H</td><td>Please look at this card and show me where the pain or discomfort is located.</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CDQ010</td><td>{Have you/Has SP} had shortness of breath either when hurrying on the level or walking up a slight hill?</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>CDQ_H</td><td>Cardiovascular Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPD035</td><td>How old {were you/was SP} when {you were/he/she was} first told that {you/he/she} had hypertension or high blood pressure?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPD058</td><td>How often {did you check your/did SP check his/her} blood pressure at home during the last 12 months?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ020</td><td>{Have you/Has SP} ever been told by a doctor or other health professional that {you/s/he} had hypertension, also called high blood pressure?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ030</td><td>{Were you/Was SP} told on 2 or more different visits that {you/s/he} had hypertension, also called high blood pressure?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ040A</td><td>Because of {your/SP's} (high blood pressure/hypertension), {have you/has s/he} ever been told to . . . take prescribed medicine?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ050A</td><td>HELP AVAILABLE (Are you/Is SP) now taking prescribed medicine</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ056</td><td>{Did you/Did SP} take {your/his/her} blood pressure at home during the last 12 months?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ059</td><td>Did a doctor or other health professional tell {you/SP} to take {your/his/her} blood pressure at home?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ060</td><td>{Have you/Has SP} ever had {your/his/her} blood cholesterol checked?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ070</td><td>About how long has it been since {you/SP} last had {your/his/her} blood cholesterol checked?  Has it been...</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ080</td><td>{Have you/Has SP} ever been told by a doctor or other health professional that {your/his/her} blood cholesterol level was high?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ090D</td><td>[To lower (your/his/her) blood cholesterol, (have/has) (you/SP) ever been told by a doctor or other health professional]... to take prescribed medicine?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>BPQ100D</td><td>(Are you/Is SP) now following this advice to take prescribed medicine?</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>BPQ_H</td><td>Blood Pressure &amp; Cholesterol</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>AGQ030</td><td>During the past 12 months, {have you/has SP} had an episode of hay fever?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCD093</td><td>In what year did {you/SP} receive {your/his/her} first transfusion?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ010</td><td>The following questions are about different medical conditions. Has a doctor or other health professional ever told {you/SP} that {you have/s/he/SP has} asthma (az-ma)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ025</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/he/she} had asthma (az-ma)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ035</td><td>{Do you/Does SP} still have asthma (az-ma)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ040</td><td>During the past 12 months, {have you/has SP} had an episode of asthma (az-ma) or an asthma attack?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ050</td><td>[During the past 12 months], {have you/has SP} had to visit an emergency room or urgent care center because of asthma (az-ma)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ053</td><td>During the past 3 months, {have you/has SP} been on treatment for anemia (a-nee-me-a), sometimes called "tired blood" or "low blood"?  [Include diet, iron pills, iron shots, transfusions as treatment.]</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ070</td><td>{Have you/Has SP} ever been told by a doctor or other health care professional that {you/s/he} had psoriasis (sore-eye-asis)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ075</td><td>{Do you/Does SP} currently have . . .</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ080</td><td>Has a doctor or other health professional ever told {you/SP} that {you were/s/he/SP was} overweight?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ082</td><td>Has a doctor or other health professional ever told {you/SP} that {you have/s/he/SP has} celiac (sele-ak) disease, also called or sprue (sproo)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ084</td><td>The next question asks about difficulties in thinking or remembering that can make a big difference in everyday activities. This does not refer to occasionally forgetting your keys or the name of someone you recently met. This refers to things like confusion or memory loss that are happening more often or getting worse. We want to know how these difficulties impact {you/SP}. During the past 12 months, {have you/has she/has he} experienced confusion or memory loss that is happening more often or is getting worse?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ086</td><td>{Are you/is SP} on a gluten-free diet?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ092</td><td>{Have you/Has SP} ever received a blood transfusion?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ149</td><td>Have {SP's} periods or menstrual (men-stral) cycles started yet?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ151</td><td>How old was {SP} when she had {her} first menstrual period?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160a</td><td>Has a doctor or other health professional ever told {you/SP} that {you/s/he} . . .had arthritis (ar-thry-tis)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160b</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had congestive heart failure?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160c</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had coronary (kor-o-nare-ee) heart disease?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160d</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had angina (an-gi-na), also called angina pectoris?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160e</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had a heart attack (also called myocardial infarction (my-o-car-dee-al in-fark-shun))?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160f</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had a stroke?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160g</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had emphysema (emph-phi-see-ma)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160k</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had chronic bronchitis?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160l</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had any kind of liver condition?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160m</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had another thyroid (thigh-roid) problem?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160n</td><td>Has a doctor or other health professional ever told {you/SP} that {you/s/he} . . .had gout?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ160o</td><td>Has a doctor or other health professional ever told {you/SP}  that {you/s/he} . . .had COPD?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ170k</td><td>{Do you/Does SP} still . . . have chronic bronchitis?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ170l</td><td>{Do you/Does SP} still . . . have any kind of liver condition?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ170m</td><td>{Do you/Does SP} still . . . have another thyroid problem?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180a</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . . had arthritis?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180b</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had congestive heart failure?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180c</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had coronary heart disease?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180d</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had angina, also called angina pectoris?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180e</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had a heart attack (also called myocardial infarction)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180f</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had a stroke?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180g</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had emphysema?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180k</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had chronic bronchitis?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180l</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had any kind of liver condition?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180m</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had another thyroid problem?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ180n</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} . . .had gout?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ195</td><td>Which type of arthritis was it?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ203</td><td>Has anyone ever told {you/SP} that {you/she/he/SP} had yellow skin, yellow eyes or jaundice? Please do not include infant jaundice, which is common during the first weeks after birth.</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ206</td><td>How old {were you/was SP} when {you were/s/he was} first told {you/s/he} had yellow skin, yellow eyes or jaundice?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ220</td><td>{Have you/Has SP} ever been told by a doctor or other health professional that {you/s/he} had cancer or a malignancy (ma-lig-nan-see) of any kind?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ230a</td><td>What kind of cancer was it?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ230b</td><td>What kind of cancer was it?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ230c</td><td>What kind of cancer was it?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ230d</td><td>What kind of cancer was it?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240a</td><td>How old (were you/was SP) when bladder cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240aa</td><td>How old (were you/was SP) when testicular cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240b</td><td>How old {were you/was SP} when blood cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240bb</td><td>How old (were you/was SP) when thyroid cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240c</td><td>How old (were you/was SP) when bone cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240cc</td><td>How old (were you/was SP) when uterine cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240d</td><td>How old (were you/was SP) when brain cancer was  first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240dd</td><td>How old (were you/was SP) when some other type of cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240dk</td><td>How old {were you/was SP} when cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240e</td><td>How old (were you/was SP) when breast cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240f</td><td>How old (were you/was SP) when cervical cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240g</td><td>How old (were you/was SP) when colon cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240h</td><td>How old (were you/was SP) when esophageal cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240i</td><td>How old (were you/was SP) when gallbladder cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240j</td><td>How old (were you/was SP) when kidney cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240k</td><td>How old (were you/was SP) when larynx or windpipe cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240l</td><td>How old (were you/was SP) when leukemia was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240m</td><td>How old (were you/was SP) when liver cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240n</td><td>How old (were you/was SP) when lung cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240o</td><td>How old (were you/was SP) when lymphoma or Hodgkins' Disease was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240p</td><td>How old (were you/was SP) when melanoma was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240q</td><td>How old (were you/was SP) when mouth, tongue, or lip cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240r</td><td>How old (were you/was SP) when cancer of the nervous system was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240s</td><td>How old (were you/was SP) when ovarian cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240t</td><td>How old (were you/was SP) when pancreatic cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240u</td><td>How old (were you/was SP) when prostate cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240v</td><td>How old (were you/was SP) when rectal cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240w</td><td>How old (were you/was SP) when non-melanoma skin cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240x</td><td>How old (were you/was SP) when the unknown kind of skin cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240y</td><td>How old (were you/was SP) when soft tissue (muscle or fat) cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ240z</td><td>How old (were you/was SP) when stomach cancer was first diagnosed?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ300a</td><td>Including living and deceased, were any of {SP's/your} close biological that is, blood relatives including father, mother, sisters or brothers, ever told by a health professional that they had a heart attack or angina (an-gi-na) before the age of 50?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ300b</td><td>Including living and deceased, were any of {SP's/your} close biological that is, blood relatives including father, mother, sisters or brothers, ever told by a health professional that they had asthma (az-ma)?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ300c</td><td>Including living and deceased, were any of {SP's/your} close biological that is, blood relatives including father, mother, sisters or brothers, ever told by a health professional that they had diabetes?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ365a</td><td>To lower {your/SP's} risk for certain diseases, during the past 12 months {have you/has s/he} ever been told by a doctor or health professional to: control {your/his/her} weight or lose weight?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ365b</td><td>To lower {your/SP's} risk for certain diseases, during the past 12 months {have you/has s/he} ever been told by a doctor or health professional to: increase {your/his/her} physical activity or exercise?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ365c</td><td>To lower {your/SP's} risk for certain diseases, during the past 12 months {have you/has s/he} ever been told by a doctor or health professional to: reduce the amount of sodium or salt in {your/his/her} diet?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ365d</td><td>To lower {your/SP's} risk for certain diseases, during the past 12 months {have you/has s/he} ever been told by a doctor or health professional to: reduce the amount of fat or calories in {your/his/her} diet?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ370a</td><td>To lower {your/his/her} risk for certain diseases, {are you/is s/he} now doing any of the following: controlling {your/his/her} weight or losing weight?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ370b</td><td>To lower {your/his/her} risk for certain diseases, {are you/is s/he} now doing any of the following: increasing {your/his/her} physical activity or exercise?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ370c</td><td>To lower {your/his/her} risk for certain diseases, {are you/is s/he} now doing any of the following: reducing the amount of sodium or salt in {your/his/her} diet?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ370d</td><td>To lower {your/his/her} risk for certain diseases, {are you/is s/he} now doing any of the following: reducing the amount of fat or calories in {your/his/her} diet?</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ380</td><td>During the past 7 days, how often{have you/has SP} had trouble remembering where {you/he/she} put things, like {your/his/her} keys or {your/his/her} wallet?  Would you say...</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>MCQ_H</td><td>Medical Conditions</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ011</td><td>The (first/next) questions are about health insurance. {Are you/Is SP} covered by health insurance or some other kind of health care plan?  [Include health insurance obtained through employment or purchased directly as well as government programs like Medicare and Medicaid that provide medical care or help pay medical bills.]</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031A</td><td>{Are you/Is SP} covered by private insurance?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031AA</td><td>No coverage of any type.</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031B</td><td>{Are you/Is SP} covered by Medicare?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031C</td><td>{Are you/Is SP} covered by Medi-Gap?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031D</td><td>{Are you/Is SP} covered by Medicaid?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031E</td><td>{Are you/Is SP} covered by SCHIP (State Children's Health Insurance Program)?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031F</td><td>{Are you/Is SP} covered by military health plan (Tricare/VA/Champ-VA)?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031G</td><td>{Are you/Is SP} covered by Indian Health Service?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031H</td><td>{Are you/Is SP} covered by state-sponsored health plan?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031I</td><td>{Are you/Is SP} covered by other government insurance?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ031J</td><td>{Are you/Is SP} covered by any single service plan?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ105</td><td>Insurance card available or not.</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ210</td><td>In the past 12 months, was there any time when {you/SP} did not have any health insurance coverage?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ260</td><td>{Do you/Does SP} have Medicare?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HIQ270</td><td>{Does this plan/Do any of these plans} cover any part of the cost of prescriptions?</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>HIQ_H</td><td>Health Insurance</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HUD080</td><td>How many different times did {you/SP} stay in any hospital overnight or longer {during the past 12 months}? (Do not count total number of nights, just total number of hospital admissions for stays which lasted 1 or more nights.)</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HUQ010</td><td>{First/Next} I have some general questions about {your/SP's} health.  Would you say {your/SP's} health in general is . . .</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HUQ020</td><td>Compared with 12 months ago, would you say {your/SP's} health is now . . .</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HUQ030</td><td>Is there a place that {you/SP} usually {go/goes} when {you are/he/she is} sick or {you/s/he} need{s} advice about {your/his/her} health?</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HUQ041</td><td>{What kind of place is it - a clinic, doctor's office, emergency room, or some other place?} {What kind of place {do you/does SP} go to most often - a clinic, doctor's office, emergency room, or some other place?}</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HUQ051</td><td>{During the past 12 months, how/How} many times {have you/has SP} seen a doctor or other health care professional about {your/his/her} health at a doctor's office, a clinic or some other place?  Do not include times {you were/s/he was} hospitalized overnight, visits to hospital emergency rooms, home visits or telephone calls.</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HUQ061</td><td>About how long has it been since {you/SP} last saw or talked to a doctor or other health care professional about {your/his/her} health?  Include doctors seen while {you were} {he/she was} a patient in a hospital.  Has it been . . .</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HUQ071</td><td>{During the past 12 months, were you/{was} SP} a patient in a hospital overnight?  Do not include an overnight stay in the emergency room.</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HUQ090</td><td>During the past 12 months, that is since {DISPLAY CURRENT MONTH} of {DISPLAY LAST YEAR}, {have you/has SP} seen or talked to a mental health professional such as a psychologist, psychiatrist, psychiatric nurse or clinical social worker about {your/his/her} health?</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>HUQ_H</td><td>Hospital Utilization &amp; Access to Care</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAAQUEX</td><td>Questionnaire source flag for weighting</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAD615</td><td>How much time {do you/does SP} spend doing vigorous-intensity activities at work on a typical day?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAD630</td><td>How much time {do you/does SP} spend doing moderate-intensity activities at work on a typical day?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAD645</td><td>How much time {do you/does SP} spend walking or bicycling for travel on a typical day?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAD660</td><td>How much time {do you/does SP} spend doing vigorous-intensity sports, fitness or recreational activities on a typical day?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAD675</td><td>How much time {do you/does SP} spend doing moderate-intensity sports, fitness or recreational activities on a typical day?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAD680</td><td>The following question is about sitting at school, at home, getting to and from places, or with friends including time spent sitting at a desk, traveling in a car or bus, reading, playing cards, watching television, or using a computer. Do not include time spent sleeping. How much time {do you/does SP} usually spend sitting on a typical day?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAD733</td><td>On average, for how long did {you/SP} play these active video games?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ605</td><td>Next I am going to ask you about the time {you spend/SP spends} doing different types of physical activity in a typical week. Think first about the time {you spend/he spends/she spends} doing work.  Think of work as the things that {you have/he has/she has} to do such as paid or unpaid work,  household chores, and yard work.  Does {your/SP's} work involve vigorous-intensity activity that causes large increases in breathing or heart rate like carrying or lifting heavy loads, digging or construction work for at least 10 minutes continuously?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ610</td><td>In a typical week, on how many days {do you/does SP} do vigorous-intensity activities as part of {your/his/her} work?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ620</td><td>Does {your/SP's} work involve moderate-intensity activity that causes small increases in breathing or heart rate such as brisk walking or carrying light loads for at least 10 minutes continuously?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ625</td><td>In a typical week, on how many days {do you/does SP} do moderate-intensity activities as part of {your/his/her} work?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ635</td><td>The next questions exclude the physical activity at work that you have already mentioned.  Now I would like to ask you about the usual way {you travel/SP travels} to and from places.  For example to school, for shopping, to work.  In a typical week  {do you/does SP} walk or use a bicycle for at least 10 minutes continuously to get to and from places?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ640</td><td>In a typical week, on how many days {do you/does SP} walk or bicycle for at least 10 minutes continuously to get to and from places?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ650</td><td>The next questions exclude the work and transport activities that you have already mentioned.  Now I would like to ask you about sports, fitness and recreational activities.  In a typical week {do you/does SP} do any vigorous-intensity sports, fitness, or recreational activities that cause large increases in breathing or heart rate like running or basketball for at least 10 minutes continuously?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ655</td><td>In a typical week, on how many days {do you/does SP} do vigorous-intensity sports, fitness or recreational activities?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ665</td><td>In a typical week {do you/does SP} do any moderate-intensity sports, fitness, or recreational activities that cause a small increase in breathing or heart rate such as brisk walking, bicycling, swimming, or volleyball for at least 10 minutes continuously?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ670</td><td>In a typical week, on how many days {do you/does SP} do moderate-intensity sports, fitness or recreational activities?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ677</td><td>In this question you can include activities done in school. On how many of the past 7 days did {you/SP} exercise or participate in physical activity for at least 20 minutes that made {you/him/her} sweat and breathe hard, such as basketball, soccer, running, swimming laps, fast bicycling, fast dancing, or similar activities?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ678</td><td>On how many of the past 7 days did {you/SP} do exercises to strengthen or tone {your/his/her} muscles, such as push-ups, sit-ups, or weight lifting?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ679</td><td>About how many minutes {do you/does SP} think you should exercise or be physically active each day for good health?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ706</td><td>I'd like to ask you some questions about {your/SP's} activities. During the past 7 days, on how many days {were you/was SP} physically active for a total of at least 60 minutes per day? Add up all the time {you/he/she} spent in any kind of physical activity that increased {your/his/her} heart rate and made {you/him/her} breathe hard some of the time.</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ710</td><td>Now I will ask you first about TV watching and then about computer use.  Over the past 30 days, on average how many hours per day did {you/SP} sit and watch TV or videos?  Would you say . . .</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ715</td><td>Over the past 30 days, on average how many hours per day did {you/SP} use a computer or play computer games outside of school? Include Playstation, Nintendo DS, or other portable video games   Would you say . . .</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ722</td><td>For the next questions, think about the sports, lessons, or physical activities {you/SP} may have done during the past 7 days? Please do not include things {you/he/she} did during the school day like PE or gym class. Did {you/SP} do any physical activities during the past 7 days?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724a</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724aa</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724ab</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724ac</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724ad</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724ae</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724af</td><td>Physical activity horseback riding</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724b</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724c</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724cm</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724d</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724e</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724f</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724g</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724h</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724i</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724j</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724k</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724l</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724m</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724n</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724o</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724p</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724q</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724r</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724s</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724t</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724u</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724v</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724w</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724x</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724y</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ724z</td><td>What physical activities did {you/SP} do during the past 7 days? {PROBE:  Did {you/he/she} do any other physical activities?}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ731</td><td>During the past 7 days, on how many days did {you/SP} play active video games such as Wii Sports, Wii Fit, Xbox 360, Xbox Kinect, Playstation 3, or Dance, Dance Revolution?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ740</td><td>The next questions ask about activities during the school year. If {you are/SP is} not currently in school, think about {your/his/her} activities when {you were/he was/she was} last in school. Are students at {your/his/her} school allowed to use school facilities during lunch or during a free or elective period, such as the gymnasium, tennis courts, weight room, or track, during school time?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ742</td><td>{Do you/Does SP} use school facilities for physical activity during school time?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ744</td><td>{Do you/does SP} have PE or gym during school days?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ746</td><td>How often {do you/does SP} have PE or gym?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ748</td><td>On average, how long is the PE or gym class?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ750</td><td>I am going to read a statement and I want you to let me know if you strongly agree, agree, neither agree nor disagree, disagree or strongly disagree with the statement. {I enjoy participating in PE or gym class.}</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ755</td><td>The following are activities that may be done before, during, or after school other than during PE or gym class. If {you are/SP is} not currently in school, think about {your/his/her} activities when {you were/he was/she was} last in school.} {Do you/Does SP} participate in school sports or physical activity clubs?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759a</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759b</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759c</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759d</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759e</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759f</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759g</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759h</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759i</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759j</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759k</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759l</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759m</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759n</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759o</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759p</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759q</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759r</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759s</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759t</td><td>In what school sports or physical activity clubs {do you/does SP} participate?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759u</td><td>Participate in martial arts</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ759v</td><td>Participate in walking</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ762</td><td>{Do you/Does SP} have recess during school days?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ764</td><td>How often {do you/does SP} have recess?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ766</td><td>On average, how long is the recess period?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ770</td><td>In the past year, did {you/SP} receive a Physical Fitness Test award, such as a President's Challenge or Fitnessgram award?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ772a</td><td>What Physical Fitness Test award did {you/SP} receive?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ772b</td><td>What Physical Fitness Test award did {you/SP} receive?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PAQ772c</td><td>What Physical Fitness Test award did {you/SP} receive?</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>PAQ_H</td><td>Physical Activity</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ020</td><td>{Do you/Does SP} have an impairment or health problem that limits {your/his/her} ability to {walk, run or play} {walk or run}?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ030</td><td>Is this an impairment or health problem that has lasted, or is expected to last 12 months or longer?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ033</td><td>{Do you/Does SP} have any impairment or health problem that requires {you/him/her} to use special equipment, such as a brace, a wheelchair, or a hearing aid (excluding ordinary eyeglasses or corrective shoes)?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ041</td><td>Does {SP} receive Special Education or Early Intervention Services?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ049</td><td>The next set of questions is about limitations caused by any long-term physical, mental or emotional problem or illness.  Please do not include temporary conditions, such as a cold [or pregnancy].  Does a physical, mental or emotional problem now keep {you/SP} from working at a job or business?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ051</td><td>{Are you/Is SP} limited in the kind or amount of work {you/s/he} can do because of a physical, mental or emotional problem?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ054</td><td>Because of a health problem, {do you/does SP} have difficulty walking without using any special equipment?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ057</td><td>{Are you/Is SP} limited in any way because of difficulty remembering or because {you/s/he} experience{s} periods of confusion?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ059</td><td>{Are you/Is SP} limited in any way in any activity because of a physical, mental or emotional problem?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061A</td><td>The next questions ask about difficulties {you/SP} may have doing certain activities because of a health problem.  By "health problem" we mean any long-term physical, mental or emotional problem or illness {not including pregnancy}.   By {yourself/himself /herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .managing {your/his/her} money [such as keeping track of {your/his/her} expenses or paying bills]?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061B</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .walking for a quarter of a mile [that is about 2 or 3 blocks]?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061C</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .walking up 10 steps without resting?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061D</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .stooping, crouching, or kneeling?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061E</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .lifting or carrying something as heavy as 10 pounds [like a sack of potatoes or rice]?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061F</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .doing chores around the house [like vacuuming, sweeping, dusting, or straightening up]?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061G</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .preparing {your/his/her} own meals?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061H</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .walking from one room to another on the same level?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061I</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .standing up from an armless straight chair?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061J</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .getting in or out of bed?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061K</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .eating, like holding a fork, cutting food or drinking from a glass?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061L</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .dressing {yourself/himself/herself}, including tying shoes, working zippers, and doing buttons?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061M</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .standing or being on {your/his/her} feet for about 2 hours?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061N</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .sitting for about 2 hours?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061O</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .reaching up over {your/his/her} head?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061P</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .using {your/his/her} fingers to grasp or handle small objects?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061Q</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .going out to things like shopping, movies, or sporting events?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061R</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .participating in social activities [visiting friends, attending clubs or meetings or going to parties]?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061S</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .doing things to relax at home or for leisure [reading, watching TV, sewing, listening to music]?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ061T</td><td>By {yourself/himself/herself} and without using any special equipment, how much difficulty {do you/does SP} have . . .pushing or pulling large objects like a living room chair?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ063A</td><td>What condition or health problem causes {you/SP} to have difficulty with or need help with {NAME OF UP TO 3 ACTIVITIES/these activities}?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ063B</td><td>What condition or health problem causes {you/SP} to have difficulty with or need help with {NAME OF UP TO 3 ACTIVITIES/these activities}?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ063C</td><td>What condition or health problem causes {you/SP} to have difficulty with or need help with {NAME OF UP TO 3 ACTIVITIES/these activities}?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ063D</td><td>What condition or health problem causes {you/SP} to have difficulty with or need help with {NAME OF UP TO 3 ACTIVITIES/these activities}?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ063E</td><td>What condition or health problem causes {you/SP} to have difficulty with or need help with {NAME OF UP TO 3 ACTIVITIES/these activities}?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PFQ090</td><td>{Do you/Does SP} now have any health problem that requires {you/him/her} to use special equipment, such as a cane, a wheelchair, a special bed, or a special telephone?</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>PFQ_H</td><td>Physical Functioning</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HEQ010</td><td>Has a doctor or other health professional ever told {you/SP} that {you have/s/he/SP has} Hepatitis B? (Hepatitis is a form of liver disease. Hepatitis B is an infection of the liver from the Hepatitis B virus (HBV).)</td><td>HEQ_H</td><td>Hepatitis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HEQ020</td><td>Please look at the drugs on this card that are prescribed for Hepatitis B. {Were you/Was/s/he/SP} ever prescribed any medicine to treat Hepatitis B?</td><td>HEQ_H</td><td>Hepatitis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HEQ030</td><td>Has a doctor or other health professional ever told {you/SP} that {you have/s/he/SP has} Hepatitis C? (Hepatitis is a form of liver disease. Hepatitis C is an infection of the liver from the Hepatitis C virus (HCV).)</td><td>HEQ_H</td><td>Hepatitis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HEQ040</td><td>Please look at the drugs on this card that are prescribed for Hepatitis C. {Were you/ Was/s/he/SP} ever prescribed any medicine to treat Hepatitis C?</td><td>HEQ_H</td><td>Hepatitis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>HEQ_H</td><td>Hepatitis</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ECD010</td><td>First I have some questions about {SP NAME's} birth. How old was {SP NAME's} biological mother when {s/he} was born?</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ECD070A</td><td>How much did {SP NAME} weigh at birth?</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ECD070B</td><td>How much did {SP NAME} weigh at birth?</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ECQ020</td><td>Did {SP NAME's} biological mother smoke at any time while she was pregnant with {him/her}?</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ECQ080</td><td>Did {SP NAME} weigh . . .</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ECQ090</td><td>Did {SP NAME} weigh . . .</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ECQ150</td><td>Are you now doing anything to help {SP} control {his/her} weight?</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>MCQ080E</td><td>Has a doctor or health professional ever told you that {SP} was overweight?</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHQ030E</td><td>How do you consider {SP} weight?</td><td>ECQ_H</td><td>Early Childhood</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID040</td><td>How old {was SP/were you} when a doctor or other health professional first told {you/him/her} that {you/he/she} had diabetes or sugar diabetes?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID060</td><td>For how long {have you/has SP} been taking insulin?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID250</td><td>How many times {have you/has SP} seen this doctor or other health professional in the past 12 months?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID260</td><td>How often {do you check your/does SP check his/her} blood for glucose or sugar?  Include times when checked by a family member or friend, but do not include times when checked by a doctor or other health professional.</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID310D</td><td>What does {your/SP's} doctor or other health professional say {your/his/her} 

blood pressure should be?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID310S</td><td>What does {your/SP's} doctor or other health professional say {your/his/her} 

blood pressure should be?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID320</td><td>One part of total serum cholesterol in {your/SP's} blood is a bad cholesterol, 

called LDL, which builds up and clogs {your/his/her} arteries. What was {your/his/her} most 

recent LDL cholesterol number?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID330</td><td>What does {your/SP's} doctor or other health professional say {your/his/her} 

LDL cholesterol should be?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID341</td><td>During the past 12 months, about how many times has a doctor or other health professional checked {your/SP's} feet for any sores or irritations?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DID350</td><td>How often {do you check your feet/does SP check (his/her) feet} for sores or irritations?  Include times when checked by a family member or friend, but do not include times when checked by a doctor or other health professional.</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ010</td><td>The next questions are about specific medical conditions. {Other than during pregnancy, {have you/has SP}/{Have you/Has SP}} ever been told by a doctor or health professional that {you have/{he/she/SP} has} diabetes or sugar diabetes?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ050</td><td>{Is SP/Are you} now taking insulin</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ060U</td><td>UNIT OF MEASURE</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ070</td><td>{Is SP/Are you} now taking diabetic pills to lower {{his/her}/your} blood sugar?  These are sometimes called oral agents or oral hypoglycemic agents.</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ080</td><td>Has a doctor ever told {you/SP} that diabetes has affected {your/his/her} eyes or that {you/s/he} had retinopathy (ret-in-op-ath-ee)?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ160</td><td>{Have you/Has SP} ever been told by a doctor or other health professional that {you have/SP has} any of the following:  prediabetes, impaired fasting glucose, impaired glucose tolerance, borderline diabetes or that {your/her/his} blood sugar is higher than normal but not high enough to be called diabetes or sugar diabetes?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ170</td><td>{Have you/Has SP} ever been told by a doctor or other health professional that {you have/s/he has} health conditions or a medical or family history that increases {your/his/her} risk for diabetes?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ172</td><td>{Do you/Does SP} feel {you/he/she} could be at risk for diabetes or prediabetes?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175A</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175B</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175C</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175D</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175E</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175F</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175G</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175H</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175I</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175J</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175K</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175L</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175M</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175N</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175O</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175P</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175Q</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175R</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175S</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175T</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175U</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175V</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175W</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes?
[Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ175X</td><td>Why {Do you/Does SP} think {you are/he is/she is} at risk for diabetes or prediabetes? [Anything else?]</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ180</td><td>{Have you/Has SP} had a blood test for high blood sugar or diabetes within the past three years?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ230</td><td>When was the last time {you/SP} saw a diabetes nurse educator or dietitian or nutritionist for {your/his/her} diabetes?  Do not include doctors or other health professionals.</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ240</td><td>Is there one doctor or other health professional {you usually see/SP usually sees} for {your/his/her} diabetes?  Do not include specialists to whom {you have/SP has} been referred such as diabetes educators, dieticians or foot and eye doctors.</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ260U</td><td>How often {do you check your/does SP check his/her} blood for glucose or sugar?  Include times when checked by a family member or friend, but do not include times when checked by a doctor or other health professional.</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ275</td><td>Glycosylated (GLY-KOH-SIH-LAY-TED) hemoglobin or the "A one C" test measures your average level of blood sugar for the past 3 months, and usually ranges between 5.0 and 13.9. During the past 12 months, has a doctor or other health professional checked {your/SP's} glycosylated hemoglobin or "A one C"?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ280</td><td>What was {your/SP's} last "A one C" level?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ291</td><td>What does {your/SP's} doctor or other health professional say {your/his/her} "A one C" level  should be?  (Pick the lowest level recommended by your health care professional.)</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ300D</td><td>Blood pressure is usually given as one number over another. What was 

{your/SP's} most recent blood pressure in numbers?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ300S</td><td>Blood pressure is usually given as one number over another. What was 

{your/SP's} most recent blood pressure in numbers?</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ350U</td><td>How often {do you check your feet/does SP check (his/her) feet} for sores or irritations?  Include times when checked by a family member or friend, but do not include times when checked by a doctor or other health professional.</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DIQ360</td><td>When was the last time {you/SP} had an eye exam in which the pupils were dilated?  This would have made {you/SP} temporarily sensitive to bright light.</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>DIQ_H</td><td>Diabetes</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>SMQFAM_H</td><td>Smoking - Household Smokers</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD460</td><td>Now I would like to ask you a few questions about smoking in this home.  How many people who live here smoke cigarettes, cigars, little cigars, pipes, water pipes, hookah, or any other tobacco product?</td><td>SMQFAM_H</td><td>Smoking - Household Smokers</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD470</td><td>Not counting decks, porches, or detached garages, how many people who live here smoke cigarettes, cigars, little cigars, pipes, water pipes, hookah, or any other tobacco product inside this home?</td><td>SMQFAM_H</td><td>Smoking - Household Smokers</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD480</td><td>(Not counting decks, porches, or detached garages) During the past 7 days, that is since last [TODAY'S DAY OF WEEK], on how many days did {anyone who lives here/you}, smoke tobacco inside this home?</td><td>SMQFAM_H</td><td>Smoking - Household Smokers</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMAQUEX2</td><td>Questionnaire Mode Flag</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD030</td><td>How old {were you/was SP} when {you/s/he} first started to smoke cigarettes fairly regularly?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD055</td><td>How old {were you/was SP} when {you/s/he} last smoked cigarettes {fairly regularly}?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD057</td><td>At that time, about how many cigarettes did {you/SP} usually smoke per day?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD093</td><td>May I please see the pack for the brand of cigarettes {you usually smoke/SP usually smokes}.</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD100BR</td><td>BRAND OF CIGARETTES SMOKED BY SP (SUB-BRAND INCLUDED IF APPLICABLE AND AVAILABLE)</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD100CO</td><td>CIGARETTE CARBON MONOXIDE CONTENT</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD100FL</td><td>CIGARETTE PRODUCT FILTERED OR NON-FILTERED</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD100LN</td><td>CIGARETTE PRODUCT LENGTH</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD100MN</td><td>CIGARETTE PRODUCT MENTHOLATED OR NON-MENTHOLATED</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD100NI</td><td>CIGARETTE NICOTINE CONTENT</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD100TR</td><td>CIGARETTE TAR CONTENT</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD630</td><td>How old were you when you smoked a whole cigarette for the first time?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD641</td><td>On how many of the past 30 days did {you/SP} smoke a cigarette?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMD650</td><td>During the past 30 days, on the days that {you/SP} smoked, about how many cigarettes did {you/s/he} smoke per day?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMDUPCA</td><td>Cigarette 12-digit Universal Product Code (UPC)</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ020</td><td>These next questions are about cigarette smoking and other tobacco use. {Have you/Has SP} smoked at least 100 cigarettes in {your/his/her} entire life?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ040</td><td>{Do you/Does SP} now smoke cigarettes?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ050Q</td><td>How long has it been since {you/SP} quit smoking cigarettes?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ050U</td><td>UNIT OF MEASURE</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ078</td><td>How soon after you wake up do you smoke?  Would you say . . .</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ621</td><td>The following questions are about cigarette smoking and other tobacco use.  Do not include cigars or marijuana.  About how many cigarettes have you smoked in your entire life?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ661</td><td>During the past 30 days, on the days that you smoked, which brand of cigarettes did you usually smoke?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ665A</td><td>Please select the Marlboro pack that looks most like the brand that you smoke. If the pack you smoke is not shown, select 'other Marlboro.'</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ665B</td><td>Please select the Camel pack that looks most like the brand that you smoke. If the pack you smoke is not shown, select 'other Camel.'</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ665C</td><td>Please select the Newport pack that looks most like the brand that you smoke. If the pack you smoke is not shown, select 'other Newport.'</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ665D</td><td>Please select the pack that looks most like the brand that you smoke. If the pack you smoke is not shown, select 'other brand of cigarette.'</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ670</td><td>During the past 12 months, have you stopped smoking for one day or longer because you were trying to quit smoking?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ848</td><td>During the past 12 months, how many times {have you/has SP} stopped smoking cigarettes because {you were/he was/she was} trying to quit smoking?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ852Q</td><td>The last time {you/SP} tried to quit, how long {were you/was he/was she} able to stop smoking?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ852U</td><td>The last time {you/SP} tried to quit, how long {were you/was he/was she} able to stop smoking?</td><td>SMQ_H</td><td>Smoking - Cigarette Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMAQUEX</td><td>Questionnaire Mode Flag.</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMDANY</td><td>Used any tobacco product last 5 days?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ681</td><td>The following questions ask about use of tobacco products in the past 5 days.  During the past 5 days, including today, did you smoke cigarettes, pipes, cigars, little cigars or cigarillos, water pipes, hookahs, or e-cigarettes?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690A</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690B</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690C</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690D</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690E</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690F</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690G</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690H</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690I</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ690J</td><td>Which of these products did {you/he/she} use?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ710</td><td>During the past 5 days, including today, on how many days did {you/he/she} smoke cigarettes?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ720</td><td>During the past 5 days, including today, on the days {you/he/she} smoked, how many cigarettes did {you/he/she} smoke each day?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ725</td><td>When did {you/he/she} smoke {your/his/her} last cigarette? Was it...</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ740</td><td>During the past 5 days, including today, on how many days did {you/he/she} smoke a pipe?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ770</td><td>During the past 5 days, including today, on how many days did {you/he/she} smoke cigars, or little cigars or cigarillos?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ800</td><td>During the past 5 days, including today, on how many days did {you/he/she} use chewing tobacco, such as Redman, Levi Garrett or Beechnut?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ817</td><td>During the past 5 days, including today, on how many days did {you/he/she} use snuff, such as Skoal, Skoal Bandits, or Copenhagen?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ830</td><td>During the past 5 days, including today, on how many days did {you/he/she} use any nicotine replacement therapy products such as nicotine patches, gum, lozenges, inhalers, or nasal sprays?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ840</td><td>When did {you/he/she} last use a nicotine replacement therapy product?  Was it . . .</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ845</td><td>During the past 5 days, including today, on how many days did {you/he/she} smoke tobacco in a water pipe or Hookah?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ849</td><td>During the past 5 days, including today, on how many days did {you/he/she} smoke an e-cigarette?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ851</td><td>Smokeless tobacco products are placed in the mouth or nose and include chewing tobacco, snuff, snus, or dissolvables.  During the past 5 days, including today, did {you/he/she} use any smokeless tobacco? (Please do not include nicotine replacement products like patches, gum, lozenge, or spray which are considered products to help {you/him/her} stop smoking.)</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ857</td><td>During the past 5 days, including today, on how many days did {you/he/she} use snus?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ861</td><td>During the past 5 days, including today, on how many days did {you/he/she} use dissolvables such as strips or orbs?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ863</td><td>During the past 5 days, including today, did {you/he/she} use any nicotine replacement therapy products such as nicotine patches, gum, lozenges, inhalers, or nasal sprays?</td><td>SMQRTU_H</td><td>Smoking - Recent Tobacco Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HOD050</td><td>How many rooms are in this home?  Count the kitchen but not the bathroom.</td><td>HOQ_H</td><td>Housing Characteristics</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HOQ065</td><td>Is this {mobile home/house/apartment} owned, being bought, rented, or occupied by some other arrangement by {you/you or someone else in your family}?</td><td>HOQ_H</td><td>Housing Characteristics</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>HOQ_H</td><td>Housing Characteristics</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PUQ100</td><td>In the past 7 days, were any chemical products used in {your/his/her} home to control fleas, roaches, ants, termites, or other insects?</td><td>PUQMEC_H</td><td>Pesticide Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>PUQ110</td><td>In the past 7 days, were any chemical products used in {your/his/her} lawn or garden to kill weeds?</td><td>PUQMEC_H</td><td>Pesticide Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>PUQMEC_H</td><td>Pesticide Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMAQUEX</td><td>Questionnaire Mode Flag.</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ856</td><td>I will now ask you about tobacco smoke in other places. During the last 7 days, {were you/was SP} working at a job or business outside of the home?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ858</td><td>While {you were/SP was} working at a job or business outside of the home, did someone else smoke cigarettes or other tobacco products indoors?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ860</td><td>{I will now ask you about smoking in other places.} During the last 7 days, did {you/SP} spend time in a restaurant?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ862</td><td>While {you were/SP was} in a restaurant, did someone else smoke cigarettes or other tobacco products indoors?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ866</td><td>During the last 7 days, {did you/SP} spend time in a bar?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ868</td><td>While {you were/SP was} in a bar, did someone else smoke cigarettes or other tobacco products indoors?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ870</td><td>During the last 7 days, did {you/SP} ride in a car or motor vehicle?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ872</td><td>While {you were/SP was} riding in a car or motor vehicle, did someone else smoke cigarettes or other tobacco products?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ874</td><td>During the last 7 days, did {you/SP} spend time in a home other than {your/his/her} own?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ876</td><td>While {you were/SP was} in a home other than {your/his/her} own, did someone else smoke cigarettes or other tobacco products indoors?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ878</td><td>During the last 7 days,{were you/was SP} in any other indoor area?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SMQ880</td><td>While {you were/SP was} in the other indoor area, did someone else smoke cigarettes or other tobacco products?</td><td>SMQSHS_H</td><td>Smoking - Secondhand Smoke Exposure</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>IND235</td><td>Monthly family income (reported as a range value in dollars).</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>IND247</td><td>Total savings or cash assets at this time for {you/NAMES OF OTHER FAMILY/your family}.</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INDFMMPC</td><td>Family monthly poverty level index categories.</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INDFMMPI</td><td>Family monthly poverty level index, a ratio of monthly family income to the HHS poverty guidelines specific to family size.</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ012</td><td>Did {you/you or any family members 16 and older} receive income in {LAST CALENDAR YEAR} from self-employment including business and farm income? [Self-employment means you worked for yourself.]</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ020</td><td>The next questions are about {your/your combined family} income.  When answering these questions, please remember that by {"income/combined family income"}, I mean {your income/your income plus the income of {NAMES OF OTHER NHANES FAMILY MEMBERS} for {LAST CALENDAR YEAR}.  Did {you/you and OTHER NHANES FAMILY MEMBERS 16+} receive income in {LAST CALENDAR YEAR} from wages and salaries? [Did {you/you or OTHER FAMILY MEMBERS 16+} get paid for work in {LAST CALENDAR YEAR}.]</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ030</td><td>When answering the next questions about different kinds of income members of your family might have received in {LAST CALENDAR YEAR}, please consider that we also want to know about family members less than 16 years old.  Did {you/you or any family members living here, that is: you or NAME(S) OF OTHER NHANES FAMILY MEMBERS} receive income in {LAST CALENDAR YEAR} from Social Security or Railroad Retirement?</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ060</td><td>Did {you/you or any family members living here} receive any disability pension [other than Social Security or Railroad Retirement] in {LAST CALENDAR YEAR}?</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ080</td><td>Did {you/you or any family members living here} receive retirement or survivor pension [other than Social Security or Railroad Retirement or disability pension] in {LAST CALENDAR YEAR}?</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ090</td><td>Did {you/you or any family members living here} receive Supplemental Security Income [SSI] in {LAST CALENDAR YEAR}?</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ132</td><td>Did {you/you or any family members living here} receive any cash assistance from a state or county welfare program such as welfare, public assistance, AFDC, or some other program in {LAST CALENDAR YEAR}?</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ140</td><td>Did {you/you or any family members living here} receive interest from savings or other bank accounts or income from dividends received from stocks or mutual funds or net rental income from property, royalties, estates, or trusts in {LAST CALENDAR YEAR}?</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ150</td><td>Did {you/you or any family members living here} receive income in {LAST CALENDAR YEAR} from child support, alimony, contributions from family or others, VA payments, worker's compensation, or unemployment compensation?</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>INQ244</td><td>Do {you/NAMES OF OTHER FAMILY/you and NAMES OF FAMILY MEMBERS} have more than $5,000 in savings at this time?  Please include money in your checking accounts.</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>INQ_H</td><td>Income</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>AUQ136</td><td>{Have you/Has SP} ever had 3 or more ear infections? Please include ear infections {you/he/she} may have had when {you were/he was/she was} a child.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>AUQ138</td><td>{Have you/Has SP} ever had a tube placed in {your/his/her} ear to drain the fluid from {your/his/her} ear?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ010</td><td>The next questions are about {your/SP's} sense of smell. During the past 12 months, {have you/has he/has she} had a problem with {your/his/her} ability to smell, such as not being able to smell things or things not smelling the way they are supposed to?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ020</td><td>How would {you/SP} rate {your/his/her} ability to smell now as compared to when {you were/he was/she was} 25 years old? Is it better, worse or is there no change?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ030</td><td>Do some smells bother {you/SP} although they do not bother other people?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ040</td><td>{Do you/Does SP} sometimes smell an unpleasant, bad or burning odor when nothing is there?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ060</td><td>How long ago {did you/did SP} first notice a problem with, or a change in, {your/his/her} ability to smell?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ070</td><td>Is the problem with {your/SP's} ability to smell always there or does it come and go?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ080</td><td>The next questions are about {your/SP's} sense of taste. During the past 12 months, {have you/has he/has she} had a problem with {your/his/her} ability to taste sweet, sour, salty or bitter foods and drinks?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ090A</td><td>I am going to read you a list of tastes in everyday foods. How {is your/is SP's} ability to taste each one of these now compared to when {you were/he was/she was} 25 years old? Would you say it is better, worse, or is there no change?  salt in foods like potato chips or pretzels.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ090B</td><td>I am going to read you a list of tastes in everyday foods. How {is your/is SP's} ability to taste each one of these now compared to when {you were/he was/she was} 25 years old? Would you say it is better, worse, or is there no change?  sourness in foods like lemons or vinegar.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ090C</td><td>I am going to read you a list of tastes in everyday foods. How {is your/is SP's} ability to taste each one of these now compared to when {you were/he was/she was} 25 years old? Would you say it is better, worse, or is there no change?  sweetness in foods like peaches or ice cream.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ090D</td><td>I am going to read you a list of tastes in everyday foods. How {is your/is SP's} ability to taste each one of these now compared to when {you were/he was/she was} 25 years old? Would you say it is better, worse, or is there no change?  bitterness in drinks like unsweetened black coffee.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ100</td><td>Is {your/SP's} ability to taste food flavors such as chocolate, vanilla or strawberry as good as when {you were/he was/she was} 25 years old?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ110</td><td>During the past 12 months {have you/has SP} had a taste or other sensation in {your/his/her} mouth that does not go away?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ120A</td><td>Please describe the taste or other sensation in {your/SP's} mouth that does not go away. Would {you/he/she} say it is...</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ120B</td><td>Please describe the taste or other sensation in {your/SP's} mouth that does not go away. Would {you/he/she} say it is...</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ120C</td><td>Please describe the taste or other sensation in {your/SP's} mouth that does not go away. Would {you/he/she} say it is...</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ120D</td><td>Please describe the taste or other sensation in {your/SP's} mouth that does not go away. Would {you/he/she} say it is...</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ120E</td><td>Please describe the taste or other sensation in {your/SP's} mouth that does not go away. Would {you/he/she} say it is...</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ120F</td><td>Please describe the taste or other sensation in {your/SP's} mouth that does not go away. Would {you/he/she} say it is...</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ120G</td><td>Please describe the taste or other sensation in {your/SP's} mouth that does not go away. Would {you/he/she} say it is...</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ120H</td><td>Please describe the taste or other sensation in {your/SP's} mouth that does not go away. Would {you/he/she} say it is...</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ140</td><td>How long ago {did you/did SP} first notice a problem with, or a change in, {your/his/her} ability to taste?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ160</td><td>{Have you/Has SP} ever discussed any problem with, or change in {your/his/her} ability to taste or smell with a health care provider?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ170</td><td>When was the last time {you/SP} /discussed any problem with {your/his/her} ability to taste or smell with a health care provider?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ180</td><td>The next question refers to treatments {you/SP} may have tried to improve {your/his/her} ability to taste or smell. Please make sure to include any treatments that {your/his/her} health care provider recommended. Also include any other treatments {you/he/she} may have read about and tried.  During the past 12 months, {have you/has SP} tried any treatments to improve {your/his/her} ability to taste or smell?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ190</td><td>During the past 12 months, {have you/has SP} experienced a problem with {your/his/her} general health, work or {your/his/her} enjoyment of life because of a problem with {your/his/her) ability to taste or smell?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ200</td><td>During the past 12 months, {have you/has SP} had any of the following ...a head cold or flu for longer than a month?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ202</td><td>During the past 12 months, {have you/has SP} had any of the following ... persistent dry mouth (not enough saliva)?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ204</td><td>During the past 12 months, {have you/has SP} had any of the following ...frequent nasal congestion from allergies?</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ210</td><td>{Have you/Has SP} ever had any of the following?  wisdom teeth removed.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ220</td><td>{Have you/Has SP} ever had any of the following?  tonsils removed.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ240</td><td>{Have you/Has SP} ever had any of the following?  a loss of consciousness because of a head injury.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ250</td><td>{Have you/Has SP} ever had any of the following?  a broken nose or other serious injury to face or skull.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CSQ260</td><td>{Have you/Has SP} ever had any of the following?  two or more sinus infections.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>CSQ_H</td><td>Taste &amp; Smell</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ505</td><td>{I'll tell you when you will need it.} For the first few questions, please answer yes or no. In the past 12 months, did you buy food from fast food or pizza places? SP interview version: In the past 12 months, did {you/SP} buy food from fast food or pizza places?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ535</td><td>The last time when you ate out or bought food at a fast-food or pizza place, did you see nutrition or health information about any foods on the menu? SP interview version: The last time when {you/SP} ate out or bought food at a fast-food or pizza place, did {you/he/she} see nutrition or health information about any foods on the menu?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ540</td><td>Did you use the information in deciding which foods to buy? SP interview version: Did {you/SP} use the information in deciding which foods to buy?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ545</td><td>{Please open your hand card booklet and turn to hand card 1 to answer the next question.} If nutrition or health information were readily available in fast food or pizza places, would you use it often, sometimes, rarely, or never, in deciding what to order? SP interview version: If nutrition or health information were readily available in fast food or pizza places, would {you/SP} use it often, sometimes, rarely, or never, in deciding what to order?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ550</td><td>[For the following questions, please answer yes or no.] In the past 12 months, did you eat at a restaurant with waiter or waitress service? SP interview version: In the past 12 months, did {you/SP} eat at a restaurant with waiter or waitress service?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ552</td><td>Think about the last time {you/SP} ate at a restaurant with a waiter or waitress. Is it a chain-restaurant?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ580</td><td>The last time you ate at a restaurant with a waiter or waitress, did you see nutrition or health information about any foods on the menu? SP interview version: Did {you/SP} see nutrition or health information about any foods on the menu?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ585</td><td>Did you use the information in deciding which foods to buy? SP interview version: Did {you/SP} use the information in deciding which foods to buy?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ590</td><td>{Please look at hand card 1 [again].} If nutrition information were readily available in restaurants with a waiter or waitress, would you use it often, sometimes, rarely, or never, in deciding what to order? SP interview version: If nutrition or health information were readily available in restaurants with a waiter or waitress, would {you/SP} use it often, sometimes, rarely, or never, in deciding what to order?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ596</td><td>Next I'm going to ask a few questions about the nutritional guidelines recommended for Americans by the federal government.  {Have you/Has SP} heard of My Plate?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ606</td><td>{Have you/Has SP} looked up the My Plate plan on the internet?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBQ611</td><td>{Have you/Has SP} tried to follow the recommendations in the My Plate plan?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD030</td><td>How old was {SP} when {he/she} completely stopped breastfeeding or being fed breastmilk?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD041</td><td>How old was {SP} when {he/she} was first fed formula?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD050</td><td>How old was {SP} when {he/she} completely stopped drinking formula?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD055</td><td>This next question is about the first thing that {SP} was given other than breast milk or formula.  Please include juice, cow's milk, sugar water, baby food, or anything else that {SP} might have been given, even water.  How old was {SP} when {he/she} was first fed anything other than breast milk or formula? (Days)</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD061</td><td>How old was {SP} when {he/she} was first fed milk?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD381</td><td>During the school year, about how many times a week {do you/does SP} usually get a complete school lunch?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD411</td><td>During the school year, about how many times a week {do you/does SP} usually get a complete breakfast at school?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD895</td><td>Next I'm going to ask you about meals.  By meal, I mean breakfast, lunch and dinner.  During the past 7 days, how many meals {did you/did SP} get that were prepared away from home in places such as restaurants, fast food places, food stands, grocery stores, or from vending machines?  {Please do not include meals provided as part of the school lunch or school breakfast./Please do not include meals provided as part of the community programs you reported earlier.}</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD900</td><td>How many of those meals {did you/did SP} get from a fast-food or pizza place?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD905</td><td>Some grocery stores sell "ready to eat" foods such as salads, soups, chicken, sandwiches and cooked vegetables in their salad bars and deli counters.  During the past 30 days, how often did {you/SP} eat "ready to eat" foods from the grocery store?  Please do not include sliced meat or cheese you buy for sandwiches and frozen or canned foods.</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBD910</td><td>During the past 30 days, how often did you {SP} eat frozen meals or frozen pizzas?  Here are some examples of frozen meals and frozen pizzas.</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ010</td><td>Now I'm going to ask you some general questions about {SP's} eating habits.  Was {SP} ever breastfed or fed breastmilk?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ073A</td><td>What type of milk was {SP} first fed?  Was it . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ073B</td><td>What type of milk was {SP} first fed?  Was it . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ073C</td><td>What type of milk was {SP} first fed?  Was it . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ073D</td><td>What type of milk was {SP} first fed?  Was it . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ073E</td><td>What type of milk was {SP} first fed? Was it . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ073U</td><td>What type of milk was {SP} first fed?  Was it . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ197</td><td>Now I'm going to ask a few questions about milk products.  Do not include their use in cooking.  In the past 30 days, how often did {you/SP} have milk to drink or on {your/his/her} cereal?  Please include chocolate and other flavored milks as well as hot cocoa made with milk.  Do not count small amounts of milk added to coffee or tea.  Would you say...</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ223A</td><td>What type of milk was it?  Was it usually . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ223B</td><td>What type of milk was it?  Was it usually . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ223C</td><td>What type of milk was it?  Was it usually . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ223D</td><td>What type of milk was it?  Was it usually . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ223E</td><td>What type of milk was it? Was it usually . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ223U</td><td>What type of milk was it?  Was it usually . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ229</td><td>The next question is about regular milk use.  A regular milk drinker is someone who uses any type of milk at least 5 times a week.  Using this definition, which statement best describes {you/SP}?...</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ235A</td><td>Now, I'm going to ask you how often {you/SP} drank milk at different times in {your/his/her} life.  How often did {you/SP} drink any type of milk, including milk added to cereal when {you were/s/he was} a child between the ages of 5 and 12 years old?  Would you say...</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ235B</td><td>Now, I'm going to ask you how often {you/SP} drank milk at different times in {your/his/her} life.  How often did {you/SP} drink any type of milk, including milk added to cereal when {you were/s/he was} a teenager between the ages of 13 and 17 years old?  Would you say...</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ235C</td><td>Now, I'm going to ask you how often {you/SP} drank milk at different times in {your/his/her} life.  How often did {you/SP} drink any type of milk, including milk added to cereal when {you were/s/he was} a young adult between the ages of 18 and 35 years old?  Would you say...</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ301</td><td>The next questions are about meals provided by community or government programs.  In the past 12 months, did {you/SP} receive any meals delivered to {your/his/her} home from community programs, "Meals on Wheels", or any other programs?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ330</td><td>In the past 12 months, did {you/SP} go to a community program or senior center to eat prepared meals?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ360</td><td>During the school year, {do you/does SP} attend a kindergarten, grade school, junior or high school?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ370</td><td>Does {your/SP's} school serve school lunches?  These are complete lunches that cost the same every day.</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ390</td><td>{Do you/Does SP} get these lunches free, at a reduced price, or {do you/does he/she} pay full price?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ400</td><td>Does {your/SP's} school serve a complete breakfast that costs the same every day?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ421</td><td>{Do you/Does SP} get these breakfasts free, at a reduced price, or {do you/does he/she} pay full price?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ424</td><td>(Do you/Does SP) get a free or reduced price meal at any summer program (he/she) attends?</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DBQ700</td><td>Next I have some questions about {your/SP?s} eating habits.  In general, how healthy is {your/his/her} overall diet?  Would you say . . .</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>DBQ_H</td><td>Diet Behavior &amp; Nutrition</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBD070</td><td>The next questions are about how much money {your family spends/you spend} on food. First I'll ask you about money spent at supermarkets or grocery stores. Then we will talk about money spent at other types of stores. During the past 30 days, how much money {did your family/did you} spend at supermarkets or grocery stores? Please include purchases made with food stamps.</td><td>CBQ_H</td><td>Consumer Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBD090</td><td>About how much money was spent on nonfood items?</td><td>CBQ_H</td><td>Consumer Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBD110</td><td>About how much money {did your family/did you} spend on food at these types of stores? (Please do not include any stores you have already told me about.)</td><td>CBQ_H</td><td>Consumer Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBD120</td><td>During the past 30 days, how much money {did your family/did you} spend on eating out? Please include money spent in cafeterias at work or at school or on vending machines, for all family members.</td><td>CBQ_H</td><td>Consumer Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CBD130</td><td>During the past 30 days, how much money {did your family/did you} spend on food carried out or delivered? Please do not include money you have already told me about.</td><td>CBQ_H</td><td>Consumer Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>CBQ_H</td><td>Consumer Behavior</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HSAQUEX</td><td>Source of Health Status Data</td><td>HSQ_H</td><td>Current Health Status</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HSD010</td><td>Next I have some general questions about {your/SP's} health. Would you say {your/SP's} health in general is . . .</td><td>HSQ_H</td><td>Current Health Status</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HSQ500</td><td>Did {you/SP} have a head cold or chest cold that started during those 30 days?</td><td>HSQ_H</td><td>Current Health Status</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HSQ510</td><td>Did {you/SP} have a stomach or intestinal illness with vomiting or diarrhea that started during those 30 days?</td><td>HSQ_H</td><td>Current Health Status</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HSQ520</td><td>Did {you/SP} have flu, pneumonia, or ear infections that started during those 30 days?</td><td>HSQ_H</td><td>Current Health Status</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HSQ571</td><td>During the past 12 months, that is, since (DISPLAY CURRENT MONTH, DISPLAY LAST YEAR), (have you/has SP) donated blood?</td><td>HSQ_H</td><td>Current Health Status</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HSQ580</td><td>How long ago was {your/SP's} last blood donation?</td><td>HSQ_H</td><td>Current Health Status</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>HSQ590</td><td>Except for tests {you/SP} may have had as part of blood donations, {have you/has he/has she} ever had {your/his/her} blood tested for the AIDS virus infection?</td><td>HSQ_H</td><td>Current Health Status</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>HSQ_H</td><td>Current Health Status</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>SLQ_H</td><td>Sleep Disorders</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SLD010H</td><td>The next set of questions is about your sleeping habits.  How much sleep {do you/does SP} usually get at night on weekdays or workdays?</td><td>SLQ_H</td><td>Sleep Disorders</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SLQ050</td><td>{Have you/Has SP} ever told a doctor or other health professional that {you have/s/he has} trouble sleeping?</td><td>SLQ_H</td><td>Sleep Disorders</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SLQ060</td><td>{Have you/Has SP} ever been told by a doctor or other health professional that {you have/s/he has} a sleep disorder?</td><td>SLQ_H</td><td>Sleep Disorders</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXD530</td><td>What is the size or dose that {you take/SP takes}?</td><td>RXQASA_H</td><td>Preventive Aspirin Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXQ510</td><td>Doctors and other health care providers sometimes recommend that {you take/SP takes) a low-dose aspirin each day to prevent heart attacks, strokes, or cancer. {Have you/Has SP} ever been told to do this?</td><td>RXQASA_H</td><td>Preventive Aspirin Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXQ515</td><td>{Are you/Is SP} now following this advice?</td><td>RXQASA_H</td><td>Preventive Aspirin Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXQ520</td><td>On {your/SP's} own, {are you/is SP} now taking a low-dose aspirin each day to prevent heart attacks, strokes, or cancer?</td><td>RXQASA_H</td><td>Preventive Aspirin Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXQ525G</td><td>How often {do you/does SP} take an aspirin? (ASA taken daily, on alternate days, or another schedule?)</td><td>RXQASA_H</td><td>Preventive Aspirin Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXQ525Q</td><td>How often {do you/does SP} take an aspirin? (Number of ASA doses taken per day or per week).</td><td>RXQASA_H</td><td>Preventive Aspirin Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXQ525U</td><td>How often {do you/does SP} take an aspirin? (ASA doses taken on daily or weekly basis?)</td><td>RXQASA_H</td><td>Preventive Aspirin Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>RXQASA_H</td><td>Preventive Aspirin Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ200</td><td>The following questions ask about use of drugs not prescribed by a doctor. Please remember that your answers to these questions are strictly confidential. The first questions are about marijuana and hashish. Marijuana is also called pot or grass. Marijuana is usually smoked, either in cigarettes, called joints, or in a pipe. It is sometimes cooked in food. Hashish is a form of marijuana that is also called 'hash.' It is usually smoked in a pipe. Another form of hashish is hash oil. Have you ever, even once, used marijuana or hashish?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ210</td><td>How old were you the first time you used marijuana or hashish?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ211</td><td>Have you ever smoked marijuana or hashish at least once a month for more than one year?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ213</td><td>How old were you when you started smoking marijuana or hashish at least once a month for one year?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ215Q</td><td>How long has it been since you last smoked marijuana or hashish at least once a month for one year?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ215U</td><td>How long has it been since you last smoked marijuana or hashish at least once a month for one year?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ217</td><td>During the time that you smoked marijuana or hashish, how often would you usually use it?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ219</td><td>During the time that you smoked marijuana or hashish, how many joints or pipes would you usually smoke in a day?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ220Q</td><td>How long has it been since you last used marijuana or hashish?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ220U</td><td>How long has it been since you last used marijuana or hashish?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ230</td><td>During the past 30 days, on how many days did you use marijuana or hashish?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ240</td><td>Have you ever used cocaine, crack cocaine, heroin, or methamphetamine?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ250</td><td>The following questions are about cocaine, including all the different forms of cocaine such as powder, 'crack', 'free base', and coca paste.  Have you ever, even once, used cocaine, in any form?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ260</td><td>How old were you the first time you used cocaine, in any form?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ270Q</td><td>How long has it been since you last used cocaine, in any form?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ270U</td><td>How long has it been since you last used cocaine, in any form?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ272</td><td>During your life, altogether how many times have you used cocaine, in any form?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ280</td><td>During the past 30 days, on how many days did you use cocaine, in any form?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ290</td><td>The following questions are about heroin.  Have you ever, even once, used heroin?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ300</td><td>How old were you the first time you used heroin?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ310Q</td><td>How long has it been since you last used heroin?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ310U</td><td>How long has it been since you last used heroin?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ320</td><td>During the past 30 days, on how many days did you use heroin?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ330</td><td>The following questions are about methamphetamine, also known as crank, crystal, ice or speed.  Have you ever, even once, used methamphetamine?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ340</td><td>How old were you the first time you used methamphetamine?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ350Q</td><td>How long has it been since you last used methamphetamine?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ350U</td><td>How long has it been since you last used methamphetamine?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ352</td><td>During your life, altogether how many times have you used methamphetamine?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ360</td><td>During the past 30 days, on how many days did you use methamphetamine?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ370</td><td>The following questions are about the different ways that certain drugs can be used.  Have you ever, even once, used a needle to inject a drug not prescribed by a doctor?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ380A</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ380B</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ380C</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ380D</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ380E</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ390</td><td>How old were you when you first used a needle to inject any drug not prescribed by a doctor?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ400Q</td><td>How long ago has it been since you last used a needle to inject a drug not prescribed by a doctor?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ400U</td><td>How long ago has it been since you last used a needle to inject a drug not prescribed by a doctor?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ410</td><td>During your life, altogether how many times have you injected drugs not prescribed by a doctor?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ420</td><td>Think about the period of your life when you injected drugs the most often.  How often did you inject then?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ430</td><td>Have you ever been in a drug treatment or drug rehabilitation program?</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>DUQ_H</td><td>Drug Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DUQ200</td><td>The following questions ask about use of drugs not prescribed by a doctor. Please remember that your answers to these questions are strictly confidential. The first questions are about marijuana and hashish. Marijuana is also called pot or grass. Marijuana is usually smoked, either in cigarettes, called joints, or in a pipe. It is sometimes cooked in food. Hashish is a form of marijuana that is also called 'hash.' It is usually smoked in a pipe. Another form of hashish is hash oil. Have you ever, even once, used marijuana or hashish?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ210</td><td>How old were you the first time you used marijuana or hashish?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ211</td><td>Have you ever smoked marijuana or hashish at least once a month for more than one year?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ213</td><td>How old were you when you started smoking marijuana or hashish at least once a month for one year?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ215Q</td><td>How long has it been since you last smoked marijuana or hashish at least once a month for one year?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ215U</td><td>How long has it been since you last smoked marijuana or hashish at least once a month for one year?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ217</td><td>During the time that you smoked marijuana or hashish, how often would you usually use it?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ219</td><td>During the time that you smoked marijuana or hashish, how many joints or pipes would you usually smoke in a day?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ220Q</td><td>How long has it been since you last used marijuana or hashish?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ220U</td><td>How long has it been since you last used marijuana or hashish?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ230</td><td>During the past 30 days, on how many days did you use marijuana or hashish?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ240</td><td>Have you ever used cocaine, crack cocaine, heroin, or methamphetamine?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ250</td><td>The following questions are about cocaine, including all the different forms of cocaine such as powder, 'crack', 'free base', and coca paste.  Have you ever, even once, used cocaine, in any form?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ260</td><td>How old were you the first time you used cocaine, in any form?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ270Q</td><td>How long has it been since you last used cocaine, in any form?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ270U</td><td>How long has it been since you last used cocaine, in any form?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ272</td><td>During your life, altogether how many times have you used cocaine, in any form?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ280</td><td>During the past 30 days, on how many days did you use cocaine, in any form?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ290</td><td>The following questions are about heroin.  Have you ever, even once, used heroin?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ300</td><td>How old were you the first time you used heroin?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ310Q</td><td>How long has it been since you last used heroin?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ310U</td><td>How long has it been since you last used heroin?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ320</td><td>During the past 30 days, on how many days did you use heroin?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ330</td><td>The following questions are about methamphetamine, also known as crank, crystal, ice or speed.  Have you ever, even once, used methamphetamine?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ340</td><td>How old were you the first time you used methamphetamine?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ350Q</td><td>How long has it been since you last used methamphetamine?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ350U</td><td>How long has it been since you last used methamphetamine?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ352</td><td>During your life, altogether how many times have you used methamphetamine?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ360</td><td>During the past 30 days, on how many days did you use methamphetamine?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ370</td><td>The following questions are about the different ways that certain drugs can be used.  Have you ever, even once, used a needle to inject a drug not prescribed by a doctor?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ380A</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ380B</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ380C</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ380D</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ380E</td><td>Which of the following drugs have you injected using a needle?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ390</td><td>How old were you when you first used a needle to inject any drug not prescribed by a doctor?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ400Q</td><td>How long ago has it been since you last used a needle to inject a drug not prescribed by a doctor?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ400U</td><td>How long ago has it been since you last used a needle to inject a drug not prescribed by a doctor?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ410</td><td>During your life, altogether how many times have you injected drugs not prescribed by a doctor?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ420</td><td>Think about the period of your life when you injected drugs the most often.  How often did you inject then?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DUQ430</td><td>Have you ever been in a drug treatment or drug rehabilitation program?</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>DUQY_H_R</td><td>Drug Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>WHQMEC_H</td><td>Weight History - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHQ030M</td><td>Do you consider yourself now to be . . .</td><td>WHQMEC_H</td><td>Weight History - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHQ500</td><td>Which of the following are you trying to do about your weight:</td><td>WHQMEC_H</td><td>Weight History - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHQ520</td><td>In the past year, how often have you tried to lose weight?  Would you say . . .</td><td>WHQMEC_H</td><td>Weight History - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALQ101</td><td>The next questions are about drinking alcoholic beverages.  Included are liquor (such as whiskey or gin), beer, wine, wine coolers, and any other type of alcoholic beverage.In any one year, {have you/has SP} had at least 12 drinks of any type of alcoholic beverage?  By a drink, I mean a 12 oz. beer, a 5 oz. glass of wine, or one and half ounces of liquor.

</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALQ110</td><td>In {your/SP's} entire life, {have you/has he/ has she} had at least 12 drinks of any type of alcoholic beverage?</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALQ120Q</td><td>In the past 12 months, how often did {you/SP} drink any type of alcoholic beverage? PROBE: How many days per week, per month, or per year did {you/SP} drink?</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALQ120U</td><td>UNIT OF MEASURE.</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALQ130</td><td>In the past 12 months, on those days that {you/SP} drank alcoholic beverages, on the average, how many drinks did {you/he/she} have?</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALQ141Q</td><td>In the past 12 months, on how many days did {you/SP} have {DISPLAY NUMBER} or more drinks of any alcoholic beverage? PROBE:  How many days per week, per month, or per year did {you/SP} have {DISPLAY NUMBER} or more drinks in a single day?</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALQ141U</td><td>UNIT OF MEASURE.</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALQ151</td><td>Was there ever a time or times in {your/SP's} life when {you/he/she} drank {DISPLAY NUMBER} or more drinks of any kind of alcoholic beverage almost every day?</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALQ160</td><td>During the past 30 days, how many times did {you/SP} drink {DISPLAY NUMBER} or more drinks of any kind of alcohol in about two hours?</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>ALQ_H</td><td>Alcohol Use</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ALD020</td><td>During your life, on how many days have you had at least one drink of alcohol?</td><td>ALQY_H_R</td><td>Alcohol Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>ALD030</td><td>During the past 30 days, on how many days did you have at least one drink of alcohol?</td><td>ALQY_H_R</td><td>Alcohol Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>ALD040</td><td>During the past 30 days, on how many days did you have {DISPLAY NUMBER} or more drinks of alcohol in a row, that is, within a couple of hours?</td><td>ALQY_H_R</td><td>Alcohol Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>ALQ010</td><td>English Text: The following questions ask about alcohol use. This includes beer, wine, wine coolers, and liquor such as rum, gin, vodka, or whiskey. This does not include drinking a few sips of wine for religious purposes. How old were you when you had your first drink of alcohol, other than a few sips?</td><td>ALQY_H_R</td><td>Alcohol Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>ALQY_H_R</td><td>Alcohol Use - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ010</td><td>Over the last 2 weeks, how often have you been bothered by the following problems: little interest or pleasure in doing things?  Would you say...</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ020</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] feeling down, depressed, or hopeless?</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ030</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] trouble falling or staying asleep, or sleeping too much?</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ040</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] feeling tired or having little energy?</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ050</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] poor appetite or overeating?</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ060</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] feeling bad about yourself - or that you are a failure or have let yourself or your family down?</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ070</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] trouble concentrating on things, such as reading the newspaper or watching TV?</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ080</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] moving or speaking so slowly that other people could have noticed?  Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual?</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ090</td><td>Over the last 2 weeks, how often have you been bothered by the following problems: Thoughts that you would be better off dead or of hurting yourself in some way?</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ100</td><td>How difficult have these problems made it for you to do your work, take care of things at home, or get along with people?</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>DPQ_H</td><td>Mental Health - Depression Screener</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>DPQ010</td><td>Over the last 2 weeks, how often have you been bothered by the following problems: little interest or pleasure in doing things?  Would you say...</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ020</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] feeling down, depressed, or hopeless?</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ030</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] trouble falling or staying asleep, or sleeping too much?</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ040</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] feeling tired or having little energy?</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ050</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] poor appetite or overeating?</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ060</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] feeling bad about yourself - or that you are a failure or have let yourself or your family down?</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ070</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] trouble concentrating on things, such as reading the newspaper or watching TV?</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ080</td><td>[Over the last 2 weeks, how often have you been bothered by the following problems:] moving or speaking so slowly that other people could have noticed?  Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual?</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ090</td><td>Over the last 2 weeks, how often have you been bothered by the following problems: Thoughts that you would be better off dead or of hurting yourself in some way?</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>DPQ100</td><td>How difficult have these problems made it for you to do your work, take care of things at home, or get along with people?</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>DPQY_H_R</td><td>Mental Health - Depression Screener - Youth</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>ACD011A</td><td>What language(s) {do you/does SP} usually speak at home?</td><td>ACQ_H</td><td>Acculturation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ACD011B</td><td>What language(s) {do you/does SP} usually speak at home?</td><td>ACQ_H</td><td>Acculturation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ACD011C</td><td>What language(s) {do you/does SP} usually speak at home?</td><td>ACQ_H</td><td>Acculturation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ACD040</td><td>Now I'm going to ask you about language use.
What language(s) {do you/does SP} usually speak at home?  {Do you/Does he/Does she} speak only Spanish, more Spanish than English, both equally, more English than Spanish, or only English?</td><td>ACQ_H</td><td>Acculturation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>ACD110</td><td>{Do you/Does SP} speak only (NON-ENGLISH LANGUAGE), more (NON-ENGLISH LANGUAGE) than English, both equally, more English than (NON-ENGLISH LANGUAGE), or only English?</td><td>ACQ_H</td><td>Acculturation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>ACQ_H</td><td>Acculturation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD010</td><td>These next questions ask about {your/SP's} height and weight at different times in {your/his/her} life.  How tall {are you/is SP} without shoes?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD020</td><td>How much {do you/does SP} weigh without clothes or shoes?
</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD050</td><td>How much did {you/SP} weigh a year ago?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080A</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080B</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080C</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080D</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080E</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080F</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080G</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080H</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080I</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080J</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080K</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080L</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080M</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080N</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080O</td><td>How did {you/SP} try to lose weight? </td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080P</td><td>How did {you/SP} try to lose weight? </td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080Q</td><td>How did {you/SP} try to lose weight? </td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080R</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080S</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080T</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD080u</td><td>How did {you/SP} try to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD110</td><td>How much did {you/SP} weigh 10 years ago?  [If you don't know {your/his/her} exact weight, please make your best guess.]</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD120</td><td>How much did {you/SP} weigh at age 25?  [If you don't know {your/his/her} exact weight, please make your best guess.]  If ( you were/she was) pregnant, how much did (you/she) weigh before (your/her) pregnancy?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD130</td><td>How tall {were you/was SP} at age 25?  [If you don't know {your/his/her} exact height, please make your best guess.]</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHD140</td><td>Up to the present time, what is the most {you have/SP has} ever weighed?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHQ030</td><td>{Do you/Does SP} consider {your/his/her}self now to be . . . [If {you are/she is} currently pregnant, what did {you/she} consider {your/her}self to be before {you were/she was} pregnant?]</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHQ040</td><td>Would {you/SP} like to weigh . . .</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHQ060</td><td>Was the change between {your/SP's} current weight and {your/his/her} weight a year ago intentional?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHQ070</td><td>During the past 12 months, {have you/has SP} tried to lose weight?</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WHQ150</td><td>How old {were you/was SP} then?  [If you don't know {your/his/her} exact age, please make your best guess.]</td><td>WHQ_H</td><td>Weight History</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHD043</td><td>What is the reason that {you have/SP has} not had a period in the past 12 months?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHD143</td><td>{Are you/Is SP} pregnant now?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHD173</td><td>How old {were you/was SP} when {you/she} delivered a baby that weighed 9 pounds or more?  (Please count stillbirths as well as live births.)</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHD180</td><td>How old {were you/was SP} at the time of {your/her} first live birth?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHD190</td><td>How old {were you/was SP} at the time of {your/her} last live birth?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHD280</td><td>{Have you/Has SP} had a hysterectomy that is, surgery to remove {your/her} uterus or womb?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ010</td><td>The next series of questions are about {your/SP's} reproductive history.  I will begin by asking about {your/SP's} periods or menstrual cycles.  How old {were you/was SP} when {you/SP} had {your/her} first menstrual period?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ020</td><td>{Were you/Was SP}...</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ031</td><td>{Have you/Has SP} had at least one menstrual period in the past 12 months? (Please do not include bleedings caused by medical conditions, hormone therapy, or surgeries.)</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ060</td><td>About how old {were you/was SP} when {you/SP} had {your/her} last menstrual period?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ070</td><td>{Were you/Was SP}...</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ074</td><td>The next questions are about {your/SP's} pregnancy history. {Have you/Has SP} ever attempted to become pregnant over a period of at least a year without becoming pregnant?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ076</td><td>{Have you/Has SP} ever been to a doctor or other medical provider because {you have/she has} been unable to become pregnant?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ078</td><td>{Have you/Has SP} ever been treated for an infection in {your/her} fallopian tubes, uterus or ovaries, also called a pelvic infection, pelvic inflammatory disease, or PID?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ131</td><td>The next questions are about {your/SP's} pregnancy history. {Have you/Has SP ever been pregnant? Please include (current pregnancy,) live births, miscarriages, stillbirths, tubal pregnancies and abortions.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ160</td><td>How many times {have you/has SP} been pregnant?  ({Again, be/Be} sure to count all {your/her} pregnancies including (current pregnancy,) live births, miscarriages, stillbirths, tubal pregnancies or abortions.)</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ162</td><td>During {any/your/SP's} pregnancy, {were you/was SP} ever told by a doctor or other health professional that {you/she} had diabetes, sugar diabetes or gestational diabetes?  Please do not include diabetes that {you/SP} may have known about before the pregnancy.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ163</td><td>How old {were you/was SP} when {you were/she was} first told {you/she} had diabetes during a pregnancy?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ166</td><td>How many vaginal deliveries {have you/has SP} had?  {Please count stillbirths as well as live births}</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ169</td><td>How many cesarean deliveries {have you/has SP} had?  (Cesarean deliveries are also known as C-sections.)  (Please count stillbirths as well as live births.)</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ171</td><td>How many of {your/her} deliveries resulted {Did {your/her} delivery result} in a live birth?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ172</td><td>{Did {your/SP's} delivery/Did any of {your/SP's} deliveries} result in a baby that weighed 9 pounds (4082 g) or more at birth?  (Please count stillbirths as well as live births.)</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ197</td><td>How many months ago did {you/SP} have {your/her} baby?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ200</td><td>{Are you/Is SP} now breast feeding a child?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ291</td><td>How old {were you/was SP} when {you/she} had {your/her} (hysterectomy/uterus removed/womb removed)?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ305</td><td>{Have you/Has SP} had both of {your/her} ovaries removed (either when {you/she} had {your/her} uterus removed or at another time)?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ332</td><td>How old {were you/was SP} when {you/she} had {your/her} ovaries removed or last ovary removed if removed at different times?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ420</td><td>Now I am going to ask you about {your/SP's} birth control history.  {Have you/Has SP} ever taken birth control pills for any reason?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ540</td><td>{Have you/Has SP} ever used female hormones such as estrogen and progesterone?  Please include any forms of female hormones, such as pills, cream, patch, and injectables, but do not include birth control methods or use for infertility.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ542A</td><td>Which forms of female hormones {have you/has SP} used.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ542B</td><td>Which forms of female hormones {have you/has SP} used.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ542C</td><td>Which forms of female hormones {have you/has SP} used.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ542D</td><td>Which forms of female hormones {have you/has SP} used.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ554</td><td>{Have you/Has SP} ever taken female hormone pills containing estrogen only (like Premarin)? (Do not include birth control pills.)</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ560Q</td><td>Not counting any time when {you/SP} stopped taking them, for how long altogether {have you taken/did you take/has she taken/did she take} pills containing estrogen only?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ560U</td><td>UNIT OF MEASURE.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ570</td><td>{Have you/Has SP} taken female hormone pills containing both estrogen and progestin (like Prempro, Premphase)? (Do not include birth control pills.)</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ576Q</td><td>Not counting any time when {you/SP} stopped taking them, for how long altogether {{have you/has SP} taken/did {you/SP} take} pills containing both estrogen and progestin?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ576U</td><td>UNIT OF MEASURE.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ580</td><td>{Have you/Has SP} ever used female hormone patches containing estrogen only?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ586Q</td><td>Not counting any time when {you/SP} stopped taking them, for how long altogether {have you used/did you use/has she used/did she use} patches containing estrogen only?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ586U</td><td>UNIT OF MEASURE.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ596</td><td>{Have you/Has SP} used female hormone patches containing both estrogen and progestin?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ602Q</td><td>Not counting any time when {you/SP} stopped taking them, for how long altogether {have you used/did you use/has she used/did she use} patches containing both estrogen and progestin?</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHQ602U</td><td>UNIT OF MEASURE.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>RHQ_H</td><td>Reproductive Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RHD043</td><td>What is the reason that {you have/SP has} not had a period in the past 12 months?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHD143</td><td>{Are you/Is SP} pregnant now?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHD280</td><td>{Have you/Has SP} had a hysterectomy that is, surgery to remove {your/her} uterus or womb?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ010</td><td>The next series of questions are about {your/SP's} reproductive history.  I will begin by asking about {your/SP's} periods or menstrual cycles.  How old {were you/was SP} when {you/SP} had {your/her} first menstrual period?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ020</td><td>{Were you/Was SP}...</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ031</td><td>{Have you/Has SP} had at least one menstrual period in the past 12 months? (Please do not include bleedings caused by medical conditions, hormone therapy, or surgeries.)</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ060</td><td>About how old {were you/was SP} when {you/SP} had {your/her} last menstrual period?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ070</td><td>{Were you/Was SP}...</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ074</td><td>The next questions are about {your/SP's} pregnancy history. {Have you/Has SP} ever attempted to become pregnant over a period of at least a year without becoming pregnant?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ076</td><td>{Have you/Has SP} ever been to a doctor or other medical provider because {you have/she has} been unable to become pregnant?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ078</td><td>{Have you/Has SP} ever been treated for an infection in {your/her} fallopian tubes, uterus or ovaries, also called a pelvic infection, pelvic inflammatory disease, or PID?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ131</td><td>The next questions are about {your/SP's} pregnancy history. {Have you/Has SP ever been pregnant? Please include (current pregnancy,) live births, miscarriages, stillbirths, tubal pregnancies and abortions.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ160</td><td>How many times {have you/has SP} been pregnant?  ({Again, be/Be} sure to count all {your/her} pregnancies including (current pregnancy,) live births, miscarriages, stillbirths, tubal pregnancies or abortions.)</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ162</td><td>During {any/your/SP's} pregnancy, {were you/was SP} ever told by a doctor or other health professional that {you/she} had diabetes, sugar diabetes or gestational diabetes?  Please do not include diabetes that {you/SP} may have known about before the pregnancy.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ163</td><td>How old {were you/was SP} when {you were/she was} first told {you/she} had diabetes during a pregnancy?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ166</td><td>How many vaginal deliveries {have you/has SP} had?  {Please count stillbirths as well as live births}</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ169</td><td>How many cesarean deliveries {have you/has SP} had?  (Cesarean deliveries are also known as C-sections.)  (Please count stillbirths as well as live births.)</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ171</td><td>How many of {your/her} deliveries resulted {Did {your/her} delivery result} in a live birth?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ172</td><td>{Did {your/SP's} delivery/Did any of {your/SP's} deliveries} result in a baby that weighed 9 pounds (4082 g) or more at birth?  (Please count stillbirths as well as live births.)</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ173</td><td>How old {were you/was SP} when {you/she} delivered a baby that weighed 9 pounds or more?  (Please count stillbirths as well as live births.)</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ180</td><td>How old {were you/was SP} at the time of {your/her} first live birth?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ190</td><td>How old {were you/was SP} at the time of {your/her} last live birth?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ197</td><td>How many months ago did {you/SP} have {your/her} baby?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ200</td><td>{Are you/Is SP} now breast feeding a child?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ291</td><td>How old {were you/was SP} when {you/she} had {your/her} (hysterectomy/uterus removed/womb removed)?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ305</td><td>{Have you/Has SP} had both of {your/her} ovaries removed (either when {you/she} had {your/her} uterus removed or at another time)?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ332</td><td>How old {were you/was SP} when {you/she} had {your/her} ovaries removed or last ovary removed if removed at different times?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ420</td><td>Now I am going to ask you about {your/SP's} birth control history.  {Have you/Has SP} ever taken birth control pills for any reason?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ540</td><td>{Have you/Has SP} ever used female hormones such as estrogen and progesterone?  Please include any forms of female hormones, such as pills, cream, patch, and injectables, but do not include birth control methods or use for infertility.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ542A</td><td>Which forms of female hormones {have you/has SP} used.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ542B</td><td>Which forms of female hormones {have you/has SP} used.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ542C</td><td>Which forms of female hormones {have you/has SP} used.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ542D</td><td>Which forms of female hormones {have you/has SP} used.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ554</td><td>{Have you/Has SP} ever taken female hormone pills containing estrogen only (like Premarin)? (Do not include birth control pills.)</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ560Q</td><td>Not counting any time when {you/SP} stopped taking them, for how long altogether {have you taken/did you take/has she taken/did she take} pills containing estrogen only?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ560U</td><td>UNIT OF MEASURE.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ570</td><td>{Have you/Has SP} taken female hormone pills containing both estrogen and progestin (like Prempro, Premphase)? (Do not include birth control pills.)</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ576Q</td><td>Not counting any time when {you/SP} stopped taking them, for how long altogether {{have you/has SP} taken/did {you/SP} take} pills containing both estrogen and progestin?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ576U</td><td>UNIT OF MEASURE.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ580</td><td>{Have you/Has SP} ever used female hormone patches containing estrogen only?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ586Q</td><td>Not counting any time when {you/SP} stopped taking them, for how long altogether {have you used/did you use/has she used/did she use} patches containing estrogen only?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ586U</td><td>UNIT OF MEASURE.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ596</td><td>{Have you/Has SP} used female hormone patches containing both estrogen and progestin?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ602Q</td><td>Not counting any time when {you/SP} stopped taking them, for how long altogether {have you used/did you use/has she used/did she use} patches containing both estrogen and progestin?</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>RHQ602U</td><td>UNIT OF MEASURE.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>RHQ_H_R</td><td>Reproductive Health - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD012N</td><td>In the last 12 months, how many people in your household received SNAP or Food Stamp benefits?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD032A</td><td>Now I am going to read you several statements that people have made about their food situation. For these statements, please tell me whether the statement was often true, sometimes true, or never true for {you/your household} in the last 12 months, that is since last {DISPLAY CURRENT MONTH}. The first statement is . . .  {I/we} worried whether {my/our} food would run out before {I/we} got money to buy more.</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD032B</td><td>[The next statement is . . .]  The food that {I/we} bought just didn't last, and {I/we} didn't have money to get more.</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD032C</td><td>[The next statement is . . .]  {I/we} couldn't afford to eat balanced meals.</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD032D</td><td>[The next statement is . . .] (I/we) relied on only a few kinds of low-cost food to feed {CHILD'S NAME / THE CHILDREN} because (I was/we were) running out of money to buy food.</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD032E</td><td>[The next statement is . . .] (I/we) couldn't feed {CHILD'S NAME / THE CHILDREN} a balanced meal, because (I/we) couldn't afford that.</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD032F</td><td>[The next statement is . . .] {CHILD'S NAME WAS /THE CHILDREN WERE} not eating enough because (I/we) just couldn't afford enough food.</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD041</td><td>In the last 12 months, since last {DISPLAY CURRENT MONTH}, did {you/you or other adults in your household} ever cut the size of your meals or skip meals because there wasn't enough money for food?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD052</td><td>How often did this happen?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD061</td><td>In the last 12 months, did you ever eat less than you felt you should because there wasn't enough money to buy food?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD071</td><td>[In the last 12 months], were you ever hungry but didn't eat because you couldn't afford enough food?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD081</td><td>[In the last 12 months], did you lose weight because you didn't have enough money for food?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD092</td><td>[In the last 12 months], did {you/you or other adults in your household} ever not eat for a whole day because there wasn't enough money for food?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD102</td><td>How often did this happen?  Would you say . . .</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD111</td><td>In the last 12 months, since {DISPLAY CURRENT MONTH} of last year, did you ever cut the size of {CHILD'S NAME's/any of the children's} meals because there wasn't enough money for food?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD122</td><td>[In the last 12 months], did {CHILD'S NAME/any of the children} ever skip meals because there wasn't enough money for food?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD132</td><td>How often did this happen?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD141</td><td>In the last 12 months, {was CHILD'S NAME/were the children} ever hungry but you just couldn't afford more food?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD146</td><td>[In the last 12 months], did {CHILD'S NAME/any of the children} ever not eat for a whole day because there wasn't enough money for food?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD151</td><td>In the last 12 months, did {you/you or any member of your household} ever get emergency food from a church, a food pantry, or a food bank, or eat in a soup kitchen?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD225</td><td>Number of days between the time the household last received Food Stamp benefit and the date of interview.</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD230</td><td>{Do you/Does any member of your household} currently receive SNAP or Food Stamp benefits?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD650ZC</td><td>Did {SP} receive benefits from WIC, that is, the Women, Infants, and Children program, in the past 12 months?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD650ZW</td><td>These next questions are about participation in programs for women with young children. Did {you/SP} personally receive benefits from WIC, that is, the Women, Infants, and Children Program, in the past 12 months?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD660ZC</td><td>Is {SP} now receiving benefits from the WIC program?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD660ZW</td><td>{Are you/Is SP} now receiving benefits from the WIC Program?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD670ZC</td><td>How long {did SP receive/has SP been receiving} benefits from the WIC program?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD670ZW</td><td>Thinking about {your/SP's} {pregnancy/recent pregnancy/most recent pregnancy/most recent pregnancies}, how long {did you receive/have you been receiving/did she receive/has she been receiving} benefits from the WIC Program?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD675</td><td>{Next are a few questions about the WIC program, that is, the Women, Infants, and Children program}  Did {SP} receive benefits from WIC when {he/she} was less than one year old?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD680</td><td>Did {SP} receive benefits from WIC when {he/she} {was/is} between the ages of 1 to {SP AGE} years old?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSDAD</td><td>Adult food security category for last 12 months</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSDCH</td><td>Child food security category for last 12 months</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSDHH</td><td>Household food security category for last 12 months</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSQ012</td><td>In the last 12 months, did {you/you or any member of your household} receive SNAP or Food Stamp benefits?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSQ162</td><td>In the last 12 months, did {you/you or any member of your household} receive benefits from the WIC program, that is, the Women, Infants and Children program?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSQ165</td><td>The next questions are about SNAP, the Supplemental Nutrition Assistance Program, formerly known as the Food Stamp Program. SNAP benefits are provided on an electronic debit card {or EBT card} {called the DISPLAY STATE NAME FOR EBT CARD}} card in STATE}. Have {you/you or anyone in your household} ever received SNAP or Food Stamp benefits?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSQ235</td><td>How much did {you/your household} receive in food stamp benefits the last time you got them?
ENTER DOLLAR AMOUNT.</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSQ690</td><td>Did {SP's} mother receive benefits from WIC, while she was pregnant with {SP}?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSQ695</td><td>What month of the pregnancy did {SP's} mother begin to receive WIC benefits?</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>FSQ_H</td><td>Food Security</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ030</td><td>The next questions are about {your/SP's} teeth and gums.  About how long has it been since {you/SP} last visited a dentist? Include all types of dentists, such as, orthodontists, oral surgeons, and all other dental specialists, as well as dental hygienists.</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ033</td><td>What was the main reason {you/SP} last visited the dentist?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ555G</td><td>We would like you to think of the time when {SP} started brushing {his/her} teeth either with your help or alone. At what age did {SP} start brushing {his/her} teeth?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ555Q</td><td>We would like you to think of the time when {SP} started brushing {his/her} teeth either with your help or alone. At what age did {SP} start brushing {his/her} teeth?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ555U</td><td>We would like you to think of the time when {SP} started brushing {his/her} teeth either with your help or alone. At what age did {SP} start brushing {his/her} teeth?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ560G</td><td>At what age did {SP} start using toothpaste?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ560Q</td><td>At what age did {SP} start using toothpaste?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ560U</td><td>At what age did {SP} start using toothpaste?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ565</td><td>Has {SP} ever received prescription fluoride drops?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ570Q</td><td>How old in months or years was {SP} when {he/she} started taking prescription fluoride drops?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ570U</td><td>How old in months or years was {SP} when {he/she} started taking prescription fluoride drops?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ575G</td><td>How old in months or years was {SP} when {he/she} stopped taking prescription fluoride drops?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ575Q</td><td>How old in months or years was {SP} when {he/she} stopped taking prescription fluoride drops?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ575U</td><td>How old in months or years was {SP} when {he/she} stopped taking prescription fluoride drops?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ580</td><td>Has {SP} ever received prescription fluoride tablets?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ585Q</td><td>How old in months or years was {SP} when {he/she} started taking prescription fluoride tablets?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ585U</td><td>How old in months or years was {SP} when {he/she} started taking prescription fluoride tablets?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ590G</td><td>How old in months or years was {SP} when {he/she} stopped taking prescription fluoride tablets?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ590Q</td><td>How old in months or years was {SP} when {he/she} stopped taking prescription fluoride tablets?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ590U</td><td>How old in months or years was {SP} when {he/she} stopped taking prescription fluoride tablets?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ610</td><td>In the past 12 months, did a dentist, hygienist or other dental professional have a direct conversation with {you/SP} about... ...the benefits of giving up cigarettes or other types of tobacco to improve {your/SP's} dental health?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ612</td><td>(In the past 12 months, did a dentist, hygienist or other dental professional have a direct conversation with {you/SP} about...) ... the dental health benefits of checking {your/his/her} blood sugar?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ614</td><td>(In the past 12 months, did a dentist, hygienist or other dental professional have a direct conversation with {you/SP} about...)  ...the importance of examining {your/his/her} mouth for oral cancer?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ620</td><td>How often during the last year (have you/ has SP) had painful aching anywhere in (your/his/her) mouth?  Would you say....</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ640</td><td>How often during the last year {have you/has SP} had difficulty doing {your/his/her} usual jobs or attending school because of problems with {your/his/her} teeth, mouth or dentures? Would you say . . .</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ680</td><td>How often during the last year {have you/has SP} been self-conscious or embarrassed because of  {your/his/her} teeth, mouth or dentures? Would you say . ..</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ770</td><td>During the past 12 months was there a time when (you/SP) needed dental care but could not get it at that time?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780A</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780B</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780C</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780D</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780E</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780F</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780G</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780H</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780I</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780J</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ780K</td><td>What were the reasons that (you/SP) could not get the dental care (you/she/he) needed?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ835</td><td>The next questions will ask about the condition of {your/SP's} teeth and some factors related to gum health.  Gum disease is a common problem with the mouth.  People with gum disease might have swollen gums, receding gums, sore or infected gums or loose teeth. {Do you/Does SP} think {you/s/he} might have gum disease?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ845</td><td>Overall, how would {you/SP} rate the health of {your/his/her} teeth and gums?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ848G</td><td>How many times {do you/does SP} brush (your/his/her} teeth in one day?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ848Q</td><td>How many times {do you/does SP} brush (your/his/her} teeth in one day?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ849</td><td>On average, how much toothpaste {do you/does SP} use when brushing {your/his/her} teeth?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ850</td><td>{Have you/Has SP} ever had treatment for gum disease such as scaling and root planing, sometimes called "deep cleaning"?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ855</td><td>{Have you/Has SP} ever had any teeth become loose on their own, without an injury?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ860</td><td>{Have you/Has SP} ever been told by a dental professional that {you/s/he} lost bone around [your/his/her} teeth?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ865</td><td>During the past three months, {have you/has SP} noticed a tooth that doesn't look right?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ870</td><td>Aside from brushing {your/his/her} teeth with a toothbrush, in the last seven days, how many days did {you/SP} use dental floss or any other device to clean between {your/his/her} teeth?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ875</td><td>Aside from brushing {your/his/her} teeth with a toothbrush, in the last seven days, how many days did {you/SP} use mouthwash or other dental rinse product that {you use/s/he uses} to treat dental disease or dental problems?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ880</td><td>{Have you/Has SP} ever had an exam for oral cancer in which the doctor or dentist pulls on {your/his/her} tongue, sometimes with gauze wrapped around it, and feels under the tongue and inside the cheeks?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ885</td><td>{Have you/Has SP} ever had an exam for oral cancer in which the doctor or dentist feels {your/his/her} neck?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ895</td><td>When did {you/SP} have {your/his/her} most recent oral or mouth cancer exam?  Was it within the past year, between 1 and 3 years ago, or over 3 years ago?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OHQ900</td><td>What type of health care professional performed {your/SP's} most recent oral cancer exam?</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>OHQ_H</td><td>Oral Health</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>FSD012N</td><td>In the last 12 months, how many people in your household received SNAP or Food Stamp benefits?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD032A</td><td>Now I am going to read you several statements that people have made about their food situation. For these statements, please tell me whether the statement was often true, sometimes true, or never true for {you/your household} in the last 12 months, that is since last {DISPLAY CURRENT MONTH}. The first statement is . . .  {I/we} worried whether {my/our} food would run out before {I/we} got money to buy more.</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD032B</td><td>[The next statement is . . .]  The food that {I/we} bought just didn't last, and {I/we} didn't have money to get more.</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD032C</td><td>[The next statement is . . .]  {I/we} couldn't afford to eat balanced meals.</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD032D</td><td>[The next statement is . . .] (I/we) relied on only a few kinds of low-cost food to feed {CHILD'S NAME / THE CHILDREN} because (I was/we were) running out of money to buy food.</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD032E</td><td>[The next statement is . . .] (I/we) couldn't feed {CHILD'S NAME / THE CHILDREN} a balanced meal, because (I/we) couldn't afford that.</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD032F</td><td>[The next statement is . . .] {CHILD'S NAME WAS /THE CHILDREN WERE} not eating enough because (I/we) just couldn't afford enough food.</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD041</td><td>In the last 12 months, since last {DISPLAY CURRENT MONTH}, did {you/you or other adults in your household} ever cut the size of your meals or skip meals because there wasn't enough money for food?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD052</td><td>How often did this happen?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD061</td><td>In the last 12 months, did you ever eat less than you felt you should because there wasn't enough money to buy food?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD071</td><td>[In the last 12 months], were you ever hungry but didn't eat because you couldn't afford enough food?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD081</td><td>[In the last 12 months], did you lose weight because you didn't have enough money for food?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD092</td><td>[In the last 12 months], did {you/you or other adults in your household} ever not eat for a whole day because there wasn't enough money for food?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD102</td><td>How often did this happen?  Would you say . . .</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD111</td><td>In the last 12 months, since {DISPLAY CURRENT MONTH} of last year, did you ever cut the size of {CHILD'S NAME's/any of the children's} meals because there wasn't enough money for food?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD122</td><td>[In the last 12 months], did {CHILD'S NAME/any of the children} ever skip meals because there wasn't enough money for food?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD132</td><td>How often did this happen?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD141</td><td>In the last 12 months, {was CHILD'S NAME/were the children} ever hungry but you just couldn't afford more food?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD146</td><td>[In the last 12 months], did {CHILD'S NAME/any of the children} ever not eat for a whole day because there wasn't enough money for food?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD151</td><td>In the last 12 months, did {you/you or any member of your household} ever get emergency food from a church, a food pantry, or a food bank, or eat in a soup kitchen?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD225</td><td>Number of days between the time the household last received Food Stamp benefit and the date of interview.</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD230</td><td>{Do you/Does any member of your household} currently receive SNAP or Food Stamp benefits?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD650ZC</td><td>Did {SP} receive benefits from WIC, that is, the Women, Infants, and Children program, in the past 12 months?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD650ZW</td><td>These next questions are about participation in programs for women with young children. Did {you/SP} personally receive benefits from WIC, that is, the Women, Infants, and Children Program, in the past 12 months?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD660ZC</td><td>Is {SP} now receiving benefits from the WIC program?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD660ZW</td><td>{Are you/Is SP} now receiving benefits from the WIC Program?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD670ZC</td><td>How long {did SP receive/has SP been receiving} benefits from the WIC program?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD670ZW</td><td>Thinking about {your/SP's} {pregnancy/recent pregnancy/most recent pregnancy/most recent pregnancies}, how long {did you receive/have you been receiving/did she receive/has she been receiving} benefits from the WIC Program?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD675</td><td>{Next are a few questions about the WIC program, that is, the Women, Infants, and Children program}  Did {SP} receive benefits from WIC when {he/she} was less than one year old?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSD680</td><td>Did {SP} receive benefits from WIC when {he/she} {was/is} between the ages of 1 to {SP AGE} years old?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSDAD</td><td>Adult food security category for last 12 months</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSDCH</td><td>Child food security category for last 12 months</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSDHH</td><td>Household food security category for last 12 months</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSQ012</td><td>In the last 12 months, did {you/you or any member of your household} receive SNAP or Food Stamp benefits?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSQ162</td><td>In the last 12 months, did {you/you or any member of your household} receive benefits from the WIC program, that is, the Women, Infants and Children program?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSQ165</td><td>The next questions are about SNAP, the Supplemental Nutrition Assistance Program, formerly known as the Food Stamp Program. SNAP benefits are provided on an electronic debit card {or EBT card} {called the DISPLAY STATE NAME FOR EBT CARD}} card in STATE}. Have {you/you or anyone in your household} ever received SNAP or Food Stamp benefits?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSQ235</td><td>How much did {you/your household} receive in food stamp benefits the last time you got them?
ENTER DOLLAR AMOUNT.</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSQ690</td><td>Did {SP's} mother receive benefits from WIC, while she was pregnant with {SP}?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>FSQ695</td><td>What month of the pregnancy did {SP's} mother begin to receive WIC benefits?</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>FSQ_H_R</td><td>Food Security - Pregnant Women</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>OCD150</td><td>(SP Interview Version) In this part of the survey I will ask you questions about {your/SP's} work experience. Which of the following {were you/was SP} doing last week . . . (Family Interview Version) The next questions are about {your/NON-SP HEAD'S/NON- SP SPOUSE'S} current job or business.  Which of the following {were you/was} {NON-SP HEAD/NON-SP SPOUSE} doing last week . . .</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCD231</td><td>What kind of business or industry is this? (For example: a TV or, radio management, retail shoe store, state labor department, farm.)</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCD241</td><td>What kind of work {were you/was SP} doing? (For example: farming, mail clerk, computer specialist.)</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCD270</td><td>About how long {have you/has SP} worked for {EMPLOYER} as a(n) {OCCUPATION}?</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCD390G</td><td>Thinking of all the paid jobs or businesses {you/SP} ever had, what kind of work {were you/was s/he} doing the longest?  (For example, electrical engineer, stock clerk, typist, farmer.)</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCD391</td><td>What kind of business or industry is this? (For example: a TV or, radio management, retail shoe store, state labor department, farm.)</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCD392</td><td>Thinking of all the paid jobs or businesses {you/SP} ever had, what kind of work {were you/was s/he} doing the longest? (For example, electrical engineer, stock clerk).</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCD395</td><td>About how long did {you/SP} work at that job or business?</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCQ180</td><td>How many hours did {you/SP} work last week at all jobs or businesses?</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCQ210</td><td>{Do you/Does SP} usually work 35 hours or more per week in total at all jobs or businesses?</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCQ260</td><td>Looking at the card, which of these best describes this job or work situation?</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCQ380</td><td>(SP Interview Version) What is the main reason {you/SP} did not work last week?

(Family Interview Version) What is the main reason {you/NON-SP HEAD/NON-SP SPOUSE} did not work last week?</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number</td><td>OCQ_H</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDCOUNT</td><td>The number of prescription medicines reported.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDDAYS</td><td>For how long have you been using or taking {PRODUCT NAME}?</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDDRGID</td><td>Generic drug code.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDDRUG</td><td>Generic drug name.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDRSC1</td><td>ICD-10-CM code 1.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDRSC2</td><td>ICD-10-CM code 2.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDRSC3</td><td>ICD-10-CM code 3.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDRSD1</td><td>ICD-10-CM code 1 description.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDRSD2</td><td>ICD-10-CM code 2 description.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDRSD3</td><td>ICD-10-CM code 3 description.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXDUSE</td><td>In the past 30 days, have you used or taken medication for which a prescription is needed?  Do not include prescription vitamins or minerals you may have already told me about.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>RXQSEEN</td><td>Was prescription container seen by interviewer?</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>RXQ_RX_H</td><td>Prescription Medications</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KID028</td><td>How many times {have you/has SP} passed a kidney stone?</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ005</td><td>Many people have leakage of urine.  The next few questions ask about urine leakage.  How often {do you/does SP} have urinary leakage?  Would {you/s/he} say . . .</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ010</td><td>How much urine {do you/does SP} lose each time?  Would {you/s/he} say . . .</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ022</td><td>{Have you/Has SP} ever been told by a doctor or other health professional that {you/s/he} had weak or failing kidneys?  Do not include kidney stones, bladder infections, or incontinence.</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ025</td><td>In the past 12 months, {have you/has SP} received dialysis (either hemodialysis or peritoneal dialysis)?</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ026</td><td>{Have you/Has SP} ever had kidney stones?</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ042</td><td>During the past 12 months, {have you/has SP} leaked or lost control of even a small amount of urine with an activity like coughing, lifting or exercise?</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ044</td><td>During the past 12 months, {have you/has SP} leaked or lost control of even a small amount of urine with an urge or pressure to urinate and {you/he/she} couldn't get to the toilet fast enough?`</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ046</td><td>During the past 12 months, {have you/has SP} leaked or lost control of even a small amount of urine without an activity like coughing, lifting, or exercise, or an urge to urinate?</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ050</td><td>During the past 12 months, how much did {your/her/his} leakage of urine bother {you/her/him}?  Please select one of the following choices:</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ052</td><td>During the past 12 months, how much did {your/her/his} leakage of urine affect {your/her/his} day-to-day activities?  Please select one of the following choices:</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ430</td><td>How frequently does this occur?  Would {you/s/he} say this occurs . . .</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ450</td><td>How frequently does this occur? Would {you/s/he} say this occurs. . .</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ470</td><td>How frequently does this occur?  Would {you/s/he} say this occurs . . .</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>KIQ480</td><td>During the past 30 days, how many times per night did {you/SP} most typically get up to urinate, from the time {you/s/he} went to bed at night until the time {you/he/she} got up in the morning.  Would {you/s/he} say</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>KIQ_U_H</td><td>Kidney Conditions - Urology</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CKD060</td><td>In the last 3 days, have {you/SP} had any muscle pain or soreness?</td><td>CKQ_H</td><td>Creatine Kinase</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CKQ010</td><td>In the past 3 days, did {you/SP} do any strenuous exercise or heavy physical work?</td><td>CKQ_H</td><td>Creatine Kinase</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CKQ020</td><td>Did it make {your/SP's} muscles sore or painful?</td><td>CKQ_H</td><td>Creatine Kinase</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CKQ030</td><td>In the past 3 days, {have you/has SP} had a muscle injury, bruise or injection? (Do not include insulin or allergy injections.)</td><td>CKQ_H</td><td>Creatine Kinase</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CKQ040</td><td>Did it make {your/SP's} muscles sore or painful?</td><td>CKQ_H</td><td>Creatine Kinase</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CKQ070Q</td><td>For how many days, weeks, months or years long {have you/has SP} had this pain, aching or soreness?</td><td>CKQ_H</td><td>Creatine Kinase</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CKQ070U</td><td>For how many days, weeks, months or years long {have you/has SP} had this pain, aching or soreness?</td><td>CKQ_H</td><td>Creatine Kinase</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>CKQ_H</td><td>Creatine Kinase</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ200A</td><td>{Do you/Does she/Does he} currently store paints or fuels inside {your/her/his} home?  Include {your/her/his} basement {and attached garage}.</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ210</td><td>First,  I would like to ask you a few questions about {your/SP's} home.  Does {your/her/his} home have an attached garage?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ220</td><td>Is the source of water for {your/her/his} home from a private well?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ231A</td><td>{Do you/Does she/Does he} currently use moth balls, moth crystals or toilet bowl deodorizers inside {your/her/his} home?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ241A</td><td>Now I am going to ask you a few questions about {your/SP's} activities over the last 48 hours.  This means today or yesterday.  In the last 48 hours, did {you/she/he} cook or bake with natural gas?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ241B</td><td>Now I am going to ask you a few questions about {your/SP's} activities over the last 48 hours.  This means today or yesterday. How long ago, in hours, did {you/she/he} cook or bake with natural gas?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ244A</td><td>In the last 48 hours, did {you/she/he} pump gas into a car or other motor vehicle {yourself/herself/ himself}?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ244B</td><td>How long ago, in hours, did {you/she/he} pump gas into a car or other motor vehicle {yourself/herself/ himself}?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ251A</td><td>In the last 48 hours, did {you/she/he} spend any time at a swimming pool, in a hot tub, or in a steam room?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ251B</td><td>How long ago, in hours, has it been since {you/she/he} spent time at a swimming pool, in a hot tub, or in a steam room?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ261A</td><td>In the last 48 hours, did {you/she/he} use dry cleaning solvents, visit a dry cleaning shop or wear clothes that had been dry-cleaned within the last week?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ261B</td><td>How long ago, in hours, has it been since {you/she/he} used dry cleaning solvents, visited a dry cleaning shop or wore clothes that had been dry-cleaned within the last week?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ265A</td><td>In the last 48 hours, did {you/she/he} smoke or spend 10 or more minutes near a person who was smoking a cigarette, cigar, or pipe?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ265B</td><td>How long ago, in hours, has it been since {you/she/he} smoked or spent 10 or more minutes near a person who was smoking a cigarette, cigar, or pipe?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ271A</td><td>In the last 48 hours, did {you/she/he} take a hot shower or bath for five minutes or longer?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ271B</td><td>How long ago, in hours, has it been since {your/SP's} last shower or hot bath?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ281A</td><td>In the last 48 hours, did {you/she/he} breathe fumes from freshly painted indoor surfaces, paints, paint thinner, or varnish?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ281B</td><td>How long ago, in hours, has it been since {you/she/he} breathed fumes from freshly painted indoor surfaces, paints, paint thinner, or varnish?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ281C</td><td>In the last 48 hours, did {you/she/he} breathe fumes from diesel fuel or kerosene?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ281D</td><td>How long ago, in hours, has it been since {you/she/he} breathed fumes from diesel fuel or kerosene?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ281E</td><td>In the last 48 hours, did {you/she/he} breathe fumes from fingernail polish?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>VTQ281F</td><td>How long ago, in hours, has it been since {you/she/he} breathed fumes from fingernail polish?</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>WTSVOC2Y</td><td>VOC Subsample Weight</td><td>VTQ_H</td><td>Volatile Toxicant (Subsample)</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFALANG</td><td>Language - Cognitive Functioning</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFASTAT</td><td>Cognitive functioning status</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDAPP</td><td>Animal Fluency: Sample Practice Pretest</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDARNC</td><td>Animal Fluency: Reason Not Done</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDAST</td><td>Animal Fluency: Score Total</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCCS</td><td>CERAD: Number of recalls completed</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCIR</td><td>CERAD: Intrusion word count Recall</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCIT1</td><td>CERAD: Intrusion word count Trial 1
</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCIT2</td><td>CERAD: Intrusion word count Trial 2</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCIT3</td><td>CERAD: Intrusion word count Trial 3
</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCRNC</td><td>CERAD: Reason Not Complete</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCSR</td><td>CERAD: Score Delayed Recall</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCST1</td><td>CERAD: Score Trial 1 Recall</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCST2</td><td>CERAD: Score Trial 2 Recall</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDCST3</td><td>CERAD: Score Trial 3 Recall</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDDPP</td><td>Digit Symbol Coding: Sample Practice Pretest</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDDRNC</td><td>Digit Symbol Coding: Reason Not Done</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>CFDDS</td><td>Digit Symbol Coding: Score</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number</td><td>CFQ_H</td><td>Cognitive Functioning </td><td>2013</td><td>2014</td><td>Questionnaire</td><td>None</td>
			</tr><tr>
				<td>OCD231R</td><td>What kind of business or industry is this? (For example: TV and radio management, retail shoe store, state labor department, farm.)</td><td>OCQ_H_R</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>OCD241R</td><td>What kind of work {were you/was SP} doing? (For example: farming, mail clerk, computer specialist.)</td><td>OCQ_H_R</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>OCD391R</td><td>What kind of business or industry is this? (For example: TV and radio management, retail shoe store, state labor department, farm.)</td><td>OCQ_H_R</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>OCD392R</td><td>Thinking of all the paid jobs or businesses {you/SP} ever had, what kind of work {were you/was s/he} doing the longest? (For example, electrical engineer, stock clerk, typist, farmer.)</td><td>OCQ_H_R</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr><tr>
				<td>SEQN</td><td>Respondent sequence number.</td><td>OCQ_H_R</td><td>Occupation</td><td>2013</td><td>2014</td><td>Questionnaire</td><td>RDC Only</td>
			</tr>
		</tbody>
	</table>
"""

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table with class 'table table-bordered table-striped'
table = soup.find('table', {'class': 'table table-bordered table-striped'})

# Extract table headers
headers = []
for th in table.find_all('th'):
    headers.append(th.text.strip())

# Extract table rows
rows = []
for tr in table.find_all('tr')[1:]:  # Skip the header row
    cells = tr.find_all('td')
    row = [cell.text.strip() for cell in cells]
    rows.append(row)

# Create a DataFrame
variable = "questionnaire"
df = pd.DataFrame(rows, columns=headers)

# Save the DataFrame to a CSV file
csv_file_path = f'data/{variable}_variable_list.csv'
df.to_csv(csv_file_path, index=False)

csv_file_path
