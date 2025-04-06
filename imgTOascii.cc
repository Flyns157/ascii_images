#include <Python.h>
#include <opencv2/opencv.hpp>
#include <Magick++.h>

// Convertit une image en art ASCII
static PyObject* image_to_ascii(PyObject* self, PyObject* args) {
    const char* input;
    int outpout_in_file;
    const char* outpout_file;
    int resize;
    double resize_percentage;
    int xsize;
    int ysize;
    int gscale;
    int nb_space;
    const char* other_ascii_gradient;

    // Parse les arguments
    if (!PyArg_ParseTuple(args, "sipisiiiiis", &input, &outpout_in_file, &outpout_file, &resize, &resize_percentage, &xsize, &ysize, &gscale, &nb_space, &other_ascii_gradient)) {
        return NULL;
    }

    // Charge l'image avec OpenCV
    cv::Mat img = cv::imread(input, cv::IMREAD_GRAYSCALE);
    if (img.empty()) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to open image file");
        return NULL;
    }

    // Redimensionne l'image si nécessaire
    if (resize) {
        cv::resize(img, img, cv::Size(xsize, ysize));
    }

    // Convertit l'image en art ASCII avec Magick++
    Magick::Image magick_img(Magick::Blob(img.data, img.total() * img.elemSize()));
    magick_img.magick("TXT");
    Magick::Blob ascii_blob;
    magick_img.write(&ascii_blob);
    std::string ascii_art(static_cast<char*>(ascii_blob.data()), ascii_blob.length());

    // Écrit l'art ASCII dans un fichier si nécessaire
    if (outpout_in_file) {
        std::ofstream out(outpout_file);
        if (!out) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to open output file");
            return NULL;
        }
        out << ascii_art;
    }

    // Retourne l'art ASCII en tant que chaîne
    return PyUnicode_FromString(ascii_art.c_str());
}

// Définit les méthodes du module
static PyMethodDef ImageToAsciiMethods[] = {
    {"image_to_ascii", image_to_ascii, METH_VARARGS, "Converts an image to ASCII art."},
    {NULL, NULL, 0, NULL}[^1^][1]
};

// Définit le module
static struct PyModuleDef ImageToAsciiModule = {
    PyModuleDef_HEAD_INIT, "ImageToAscii", NULL, -1, ImageToAsciiMethods
};

// Initialise le module
PyMODINIT_FUNC PyInit_ImageToAscii(void) {
    return PyModule_Create(&ImageToAsciiModule);
}
