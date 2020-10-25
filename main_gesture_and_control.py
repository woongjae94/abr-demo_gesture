if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.start()

    model = TFModel()
    cam = RScam()
    multi_device = Multi_device()

    print(eval(cam.args.debug))

    multi_device.main_loop()