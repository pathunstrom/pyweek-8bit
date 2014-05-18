import dispatch
import model
import view
import controller

def run():
    dispatcher = dispatch.Dispatch()
    game_model = model.engine.GameEngine(dispatcher)
    game_controller = controller.controller.Controller(dispatcher)
    keyboard_controller = controller.controller.PygameController(
        game_controller, game_model)
    graphics = view.GraphicalView(dispatcher, game_model)

    game_model.run()


if __name__ == '__main__':
    run()