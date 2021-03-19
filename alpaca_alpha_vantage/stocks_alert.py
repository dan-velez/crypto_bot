# stocks_alert.py - Send alert via email. Create stocks gmail.


def alert(vsymb, vmesg, vchange, vprice):
    "Alert user that a symbol is spiking."
    try:
        import smtplib
        #vpass = "=pM3XBx4S^!p"
        #vuname = "dv.stocks.bot@gmail.com"
        vpass = "+-MT8ZAQw@5C"
        vuname = "chili.sauce.1869@gmail.com"
        # Create message,
        vfrom = "Trader Bot"
        vto = vuname
        #vto = 'daniel.velez@anikasystems.com'
        vto = 'chili.sauce.1869@gmail.com' # TODO: Use stocks account.
        vsubj = "%s UP %s%% (%s)" % (vsymb, vchange, vmesg)
        vbody = "%s has gone up %s%%. It is now worth $%s. Action: %s" % (vsymb, vchange, vprice, vmesg)
        vmessage = """\
From: %s
To: %s
Subject: %s

%s
https://www.marketwatch.com/investing/stock/%s
""" % (vfrom, vto, vsubj, vbody, vsymb)

        # print("[%s]" % vmessage)
        # Send email.
        vserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        vserver.login(vuname, vpass)
        vserver.sendmail(vfrom, vto, vmessage)
        vserver.close()
        print("[* stock_wait_sell] Alert [%s] sent to %s" % (vsubj, vto))
    except Exception as e:
        print("[* stock_wait_sell] Could not send alert: %s" % e)


if __name__ == "__main__":
    alert("INPX", "SELL", "25", "0.10")