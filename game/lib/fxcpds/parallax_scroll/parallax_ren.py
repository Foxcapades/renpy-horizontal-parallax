import renpy  # type: ignore
from renpy import Transform  # type: ignore

"""renpy
init python:
"""


class ParallaxScroll(Transform):
    """
    Scrolling Image with a configurable parallax effect.
    """

    def __init__(
        self,
        dimensions: tuple[int, int],
        *layers: tuple[renpy.Displayable | str, float],
        **kwargs
    ) -> None:
        """
        Initializes the new ParallaxScroll instance with the given arguments.


        Arguments
        ---------
        dimensions : tuple[int, int]
            A two-tuple containing the width and height of the displayable in
            the format "(width, height)".

        *layers : tuple[Displayable, float]
            One or more two-tuples that each contain a displayable to render
            and a float which represents the scrolling speed of the layer.

            The first value of each tuple MUST be either an instance of
            renpy.Displayable (Composite, Image, Transform, etc.) or a string
            representing the name of or path to a defined image or an image
            file.

            The second value of each tuple MUST be a float value between `0.0`
            and `1.0` inclusive.  This value represents the percent of the
            layer image's width that will scroll across the screen per second.

            The layers are ordered back to front, meaning the first given layer
            will be the furthest from the player while the last given layer will
            be the closest.


        Keyword Arguments
        -----------------
        direction : "left" | "right"
            Controls the direction the ParallaxScroll layers will scroll.

            A value of "left" means the layers will scroll from right to left,
            where a value of "right" means the layers will scroll from left to
            right.

            Any other value passed as the `direction` argument will cause an
            exception to be raised.

            Defaults to "left".

        render_delay : float
            Controls the delay between ParallaxScroll rerenders.

            Defaults to 0.01
        """

        if (not isinstance(dimensions, tuple)) or len(dimensions) != 2:
            raise Exception(
                'argument "dimensions" must be a two-tuple containing a width '
                'and a height in the form "(width, height)"'
            )

        if not (isinstance(dimensions[0], int) or isinstance(dimensions[0], float)):
            raise Exception(
                'argument "dimensions" value 1 was not an int or a float value.'
            )

        if not (isinstance(dimensions[1], int) or isinstance(dimensions[1], float)):
            raise Exception(
                'argument "dimensions" value 2 was not an int or a float value.'
            )

        if 'crop' in kwargs:
            raise Exception('argument "crop" is not permitted.')

        self.__child = _ParallaxScrollContainer(dimensions, *layers, **kwargs)

        if 'direction' in kwargs:
            del kwargs['direction']

        if 'render_delay' in kwargs:
            del kwargs['render_delay']

        super(ParallaxScroll, self).__init__(self.__child, **kwargs, crop=(0, 0, dimensions[0], dimensions[1]))


class _ParallaxScrollContainer(renpy.Displayable):
    """
    Creator Defined Displayable representing a layered scrolling image with
    a configurable parallax effect.

    Private Properties
    ------------------
    _render_delay : float
        Delay a a fraction of a second between re-renders of the displayable.

    _width : int
        Displayable render width.

    _height : int
        Displayable render height.

    _layers : list[_ParallaxScrollLayer]
        A list of the layers that this displayable is composed of.
    """

    def __init__(
        self,
        dimensions: tuple[int, int],
        *layers: tuple[renpy.Displayable, float],
        **kwargs
    ) -> None:
        """
        Initializes the new _ParallaxScrollContainer instance with the given
        arguments.

        Arguments
        ---------
        dimensions : tuple[int, int]
            A two-tuple containing the width and height of the displayable in
            the format "(width, height)".

        *layers : tuple[Displayable, float]
            One or more two-tuples that each contain a displayable to render
            and a float which represents the scrolling speed of the layer.

            The first value of each tuple MUST be either an instance of
            renpy.Displayable (Composite, Image, Transform, etc.) or a string
            representing the name of or path to a defined image or an image
            file.

            The second value of each tuple MUST be a float value between `0.0`
            and `1.0` inclusive.  This value represents the percent of the
            layer image's width that will scroll across the screen per second.

            The layers are ordered back to front, meaning the first given layer
            will be the furthest from the player while the last given layer will
            be the closest.


        Keyword Arguments
        -----------------
        direction : "left" | "right"
            Controls the direction the ParallaxScroll layers will scroll.

            A value of "left" means the layers will scroll from right to left,
            where a value of "right" means the layers will scroll from left to
            right.

            Any other value passed as the `direction` argument will cause an
            exception to be raised.

            Defaults to "left".

        render_delay : float
            Controls the delay between ParallaxScroll rerenders.

            Defaults to 0.01
        """
        super(_ParallaxScrollContainer, self).__init__(**kwargs)

        self._validate_layers(layers)

        left = self._require_is_left(kwargs)

        self._render_delay = self._require_render_delay(kwargs)
        self._width, self._height = dimensions

        self._layers = [
            _ParallaxScrollLayer(layer[0], layer[1], self._width, left)
            for layer in layers
        ]

    def render(self, width: int, height: int, st: float, at: float) -> renpy.Render:
        render = renpy.Render(self._width, self._height)

        for layer in self._layers:
            layer.update(at)
            layer.render(render, width, height, st, at)

        renpy.redraw(self, self._render_delay)

        return render

    def visit(self) -> renpy.Displayable:
        return [ layer.displayable for layer in self._layers ]

    def _validate_layers(self, layers: tuple[tuple[renpy.Displayable | str, float], ...]) -> None:
        if len(layers) < 1:
            raise Exception(
                'argument "layers" must be a list containing one or more'
                ' two-tuples of a Displayable to render and a float'
                ' representing the layer\'s scrolling speed in the form'
                ' "(displayable, speed)".'
            )

        for i, layer in enumerate(layers):
            self._validate_layer(i, layer)

    def _validate_layer(self, i: int, layer: tuple[renpy.Displayable | str, float]) -> None:
        if not (isinstance(layer, tuple) and len(layer) == 2):
            raise Exception(
                'argument "layers" value number ' + str(i + 1) + ' was not'
                ' a tuple value.  "layers" must contain only two-tuples of'
                ' a Displayable to render and a float representing the'
                ' speed of the layer\'s scrolling speed in the form'
                ' "(displayable, speed)".'
            )

        if not (isinstance(layer[0], renpy.display.core.Displayable) or isinstance(layer[0], str)):
            raise Exception(
                'argument "layers" value number ' + str(i + 1) +
                ' contained a value at position 1 that was neither a'
                ' Displayable nor a string value.'
            )

        if not (isinstance(layer[1], float) or isinstance(layer[1], int)):
            raise Exception(
                'argument "layers" value number ' + str(i + 1) +
                ' contained a value at position 2 that was neither a float'
                ' nor an int value.'
            )

        if layer[1] < 0.0:
            raise Exception(
                'argument "layers" value number ' + str(i + 1) + ' was'
                ' less than zero.  Speed values MUST be greater than or'
                ' equal to 0.0'
            )

        if layer[1] > 1.0:
            raise Exception(
                'argument "layers" value number ' + str(i + 1) + ' was'
                ' greater than one.  Speed values MUST be less than or'
                ' equal to 1.0'
            )

    def _require_is_left(self, kwargs: dict[str, any]) -> bool:
        if "direction" in kwargs:
            if kwargs['direction'] != "left" and kwargs['direction'] != "right":
                raise Exception(
                    'argument "direction" must one of the values "left" or'
                    ' "right"'
                )
            return kwargs['direction'] == "left"
        else:
            return True

    def _require_render_delay(self, kwargs: dict[str, any]) -> float:
        if "render_delay" in kwargs:
            if not (isinstance(kwargs["render_delay"], float) or isinstance(kwargs["render_delay"], int)):
                raise Exception(
                    'argument "render_delay" must be a float or an int value'
                )
            return float(kwargs['render_delay'])
        else:
            return 0.01


class _ParallaxScrollLayer:
    """
    Represents a single layer that is part of a scrolling image with a parallax
    effect.

    Private Properties
    ------------------
    _width : int
        Width of the displayable that this layer is based on.

    _height : int
        Height of the displayable that this layer is based on

    _xoffset : float
        Offset of this layer's displayable render position from zero.  This
        value will go to a minimum of negative `self._width` when scrolling left
        and go to a maximum lf `self._width` when scrolling right.

    _last_time : float
        Timestamp of the last update as a render time float in seconds.  This
        value is used to calculate how much the layer should move to keep a
        constant rate of `self._speed`.

    _speed : float
        How much of `self._width` the layer should move per second.  For
        example, if this value is `0.2` then this layer will scroll 20% of it's
        width in the target direction.

    _max_width : int
        Width cutoff for rendering.  This value is used to determine how many
        times the base displayable should repeat to fill the horizontal space
        of the parent displayable.

    _left : bool
        Whether this layer is scrolling right to left.
    """
    def __init__(
        self,
        displayable: renpy.Displayable | str,
        speed: float,
        max_width: int,
        left: bool,
    ) -> None:
        if isinstance(displayable, str):
            self._displayable = renpy.displayable(displayable)
        elif isinstance(displayable, renpy.display.core.Displayable):
            self._displayable = displayable
        else:
            raise Exception("invalid state")

        self._width: int = -1
        self._height: int = -1
        self._xoffset: float = 0.0
        self._last_time: float = 0.0
        self._speed: float = speed
        self._max_width: int = max_width
        self._left: bool = left

    @property
    def width(self) -> int:
        """
        The width of the displayable backing this layer.
        """
        self._lazy_dimensions()
        return self._width

    @property
    def height(self) -> int:
        """
        The height of the displayable backing this layer.
        """
        self._lazy_dimensions()
        return self._height

    @property
    def displayable(self) -> renpy.Displayable:
        """
        The displayable backing this layer.
        """
        return self._displayable

    def update(self, at: float) -> None:
        """
        Updates the scroll position of this layer.

        Arguments
        ---------
        at : float
            Display time for the parent displayable.  This value is used to
            calculate how much the layer should move based on the previous time
            to keep a smooth or consistent motion.
        """
        delta = at - self._last_time
        self._last_time = at
        percent = self._clamp(delta * self._speed)

        self._lazy_dimensions()

        if self._left:
            self._update_left(percent)
        else:
            self._update_right(percent)

    def render(self, render: renpy.Render, width: int, height: int, st, at) -> None:
        """
        Renders this layer.

        Arguments
        ---------
        render : renpy.Render
            Parent render that this layer will be displayed in.

        width : int
            Amount of horizontal space available to the parent displayable, in
            pixels.

        height : int
            Amount of vertical space available to the parent displayable, in
            pixels.

        st : float
            The shown timebase in seconds.  The shown timebase begins when the
            parent displayable is first shown on the screen.

        at : float
            The animation timebase, in seconds.  The animation timebase begins
            when an image with the same tag was shown without being hidden.
            When the parent displayable is shown without a tag, this is the same
            as the shown timebase.
        """
        l_render = renpy.render(self._displayable, width, height, st, at)

        if self._left:
            self._render_left(render, l_render)
        else:
            self._render_right(render, l_render)


    def _update_left(self, percent: float) -> None:
        self._xoffset -= self._width * percent

        while self._xoffset < -self._width:
            self._xoffset += self._width

    def _update_right(self, percent: float) -> None:
        self._xoffset += self._width * percent

        x = self._width + self._max_width

        while self._xoffset > x:
            self._xoffset -= self._width

    def _render_left(self, render: renpy.Render, l_render: renpy.Render) -> None:
        render.blit(l_render, (self._xoffset, 0))

        width = self._width + self._xoffset

        while width < self._max_width:
            render.blit(l_render, (width, 0))
            width += self._width

    def _render_right(self, render: renpy.Render, l_render: renpy.Render) -> None:
        position = self._max_width - self._width + self._xoffset

        render.blit(l_render, (position, 0))

        while position > 0:
            position -= self._width
            render.blit(l_render, (position, 0))

    def _lazy_dimensions(self) -> None:
        if self._width > 0:
            return

        size = renpy.render(self._displayable, 0, 0, 0, 0).get_size()
        self._width: int = size[0]
        self._height: int = size[1]

        if self._width == 0 or self._height == 0:
            raise Exception("displayable for _ParallaxScrollLayer has a width and/or height of 0")

    @staticmethod
    def _clamp(percent: float) -> float:
        if percent < 0.0:
            return 0.0
        elif percent > 1.0:
            return 1.0
        else:
            return percent
