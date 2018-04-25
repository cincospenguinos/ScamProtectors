#!/usr/bin/env ruby
require 'gmail'

text = <<-TEXT
FROM:- MRS HELLEN P. ANYANWU.
JOHANNESBURG SOUTH AFRICA.
Dear Sir/Madam,
I am writing to you out of a painful heart and situation, which our 
president has caused us the farmers. I know   you may be surprised to receive this letter from me since you do not know me personally. I am HELLEN P. ANYANWU the wife of MR. EVANS PETERSON  ANYANWU, who was recently murdered in the land dispute in Zimbabwe.
 I got your contact through network online hence decided to write to you. Before the death of my husband, he was the onwer of (ANYANWU INDUSTRIES PTY LTD) in Zimbabwe a Company which specialize in Agriculture and the Supply of Agricultural Equipments. Before his murder  had taken me to South Africa to deposit the sum of USD$15. Million (Fifteen MILLION   United States Dollars) in one of the private Security Companies, as if he foresaw  the looming danger in Zimbabwe. This money was deposited in a box as to avoid more demurrage from the Security Company. This amount was meant for the purchase of new machines and chemicals for the farms and establishment of a new farm in Swaziland a small country  near Zimbabwe here. 
This land problem came when Zimbabwe President MR. ROBERT MUGABE introduced a New Land Act reform, which Wholly affected the rich white farmers and some few Black farmers. This resulted to killing and mob action by Zimbabwean war veterans and some lunatics in the society. In fact, a lot of people were killed because of this land reform act for which my husband was one of the victims.
It is against this background that my family and I who are currently staying in South Africa decided to transfer my husband money to a 
foreign Country since the law of South Africa prohibits refugees to open any bank account or to be involved in any financial transaction throughout the territorial zones of South Africa.
As his wife, I am saddled with the responsibility of seeking for a 
genuine foreign Account where this money could be transferred into without the knowledge of my government who are bent on my family, or I can arrange with the security company to send the money as a consignment to their sister company in your country for you to go there and sign it out.
I must also let you know that this transaction is 100% risk free. If 
you accept to assist me and my family then the lawyer or consultant will help me and you in opening a non resident account in your name   which will aid us in transferring the money into any account you will nominate overseas or you provide your address were the security company can ship it as a consignment to you. 
This money I intend to use for investment and growth in your country. I have two options; firstly you can choose to have certain Percentage of the money for nominating your account for this transaction, or you can go into partnership with me for proper profitable investment of this money in your country. Whichever the option you want, feel free to notify me. I have also mapped out 5% of this money for all kinds of expenses we might incur in the   process of this transaction.
If you do not prefer a partnership, I am willing to give you 25% of the 
total money while remaining 70% will remain for my family and me. If 
you are really capable and willing to assist me, please contact me immediately with the above telephone number with which I have sent you this message.Finally, please treat this matter as urgent as possible. I am in dire need to leave this country with my family soonest.
Thanks for your mutual co-operation.
I expect your soonest response.
Best regards,
MRS. HELLEN ANYANWU. Please send your response to (hellenpeterson@gmail.com)
(For the family).
From r  Sun Jul 16 13:27:23 2006
TEXT

subject_line = 'SCAM_TEST_' + ('a'..'z').to_a.shuffle[0,8].join

Gmail.connect!(ENV['SP_GMAIL_USERNAME'], ENV['SP_GMAIL_PASSWORD']) do |gmail|
  gmail.deliver do
    to ENV['SP_GMAIL_USERNAME']
    subject subject_line
    text_part { body text }
  end
end
