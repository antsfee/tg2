from pylons.wsgiapp import PylonsApp
from pylons.util import class_name_from_module_name
import sys

class TGApp(PylonsApp):

    def find_controller(self, controller):
        """Locates a controller by attempting to import it then grab
        the SomeController instance from the imported module.

        Override this to change how the controller object is found once
        the URL has been resolved.

        """
        # Check to see if we've cached the class instance for this name
        if controller in self.controller_classes:
            return self.controller_classes[controller]

        root_module_path = self.config['paths']['root']
        controller_path = self.config['paths']['controllers']

        #remove the part of the path we expect to be the root part (plus one '/')
        assert controller_path.startswith(root_module_path)
        controller_path = controller_path[len(root_module_path)+1:]

        #attach the package
        pylons_package = self.config['pylons.package']
        full_module_name = pylons_package+'.'+controller_path.replace('/', '.')+'.'+controller.replace('/', '.')

        print full_module_name

        # Hide the traceback here if the import fails (bad syntax and such)
        __traceback_hide__ = 'before_and_this'

        __import__(full_module_name)
        module_name = controller.split('/')[-1]
        class_name = class_name_from_module_name(module_name) + 'Controller'
        if self.log_debug:
            log.debug("Found controller, module: '%s', class: '%s'",
                      full_module_name, class_name)
        self.controller_classes[controller] = mycontroller = \
            getattr(sys.modules[full_module_name], class_name)
        return mycontroller